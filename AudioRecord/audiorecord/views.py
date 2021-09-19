from django.contrib.auth.signals import user_logged_in
from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .models import CommentOnAudio, AudioTable, LikeOnAudio
from .serializers import (UserSerializer, RegisterSerializer, CommentOnAudioSerializer,
    AudioTableSerializer, LikeOnAudioSerializer)
from django.contrib.auth import login, logout
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from rest_framework.permissions import IsAuthenticated

# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        token_limit_per_user = self.get_token_limit_per_user()
        if token_limit_per_user is not None:
            now = timezone.now()
            token = request.user.auth_token_set.filter(expiry__gt=now)
            if token.count() >= token_limit_per_user:
                return Response(
                    {"error": "Maximum amount of tokens allowed per user exceeded."},
                    status=status.HTTP_403_FORBIDDEN
                )
        token_ttl = self.get_token_ttl()
        instance, token = AuthToken.objects.create(request.user, token_ttl)
        user_logged_in.send(sender=request.user.__class__,
                            request=request, user=request.user)
        data = self.get_post_response_data(request, token, instance)
        data['user_id'] = request.user.id
        return Response(data)


class AudioTableAPI(generics.ListCreateAPIView):
    queryset = AudioTable.objects.all()
    serializer_class = AudioTableSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = AudioTableSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        audio = serializer.save()
        return Response({
            "audio_data": AudioTableSerializer(
                audio, context=self.get_serializer_context()).data,
            "message": "Data Created Succesfully"
        })


class LikeAPI(generics.ListCreateAPIView):
    queryset = LikeOnAudio.objects.all()
    serializer_class = LikeOnAudioSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = LikeOnAudioSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        like_on_audio = serializer.save()
        audio = AudioTable.objects.filter(id=request.data['audio_id']).last()
        if audio: 
            audio.likes_on_audio.add(like_on_audio)
            return Response({
                "like_data": LikeOnAudioSerializer(
                    like_on_audio, context=self.get_serializer_context()).data,
                "message": "Liked Succesfully"
            })
        return Response({
            "message": "No audio Found"
        })


class CommentAPI(generics.ListCreateAPIView):
    queryset = CommentOnAudio.objects.all()
    serializer_class = CommentOnAudioSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = CommentOnAudioSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        comment_on_audio = serializer.save()
        audio = AudioTable.objects.filter(id=request.data['audio_id']).last()
        if not audio:
            return Response({
                "message": "No audio Found"
            })
        comment_id = CommentOnAudio.objects.filter(id=request.data['comment_id']).last()
        if comment_id:
            comment_id.comment_tree.add(comment_on_audio)
            return Response({
                "comment_data": CommentOnAudioSerializer(
                    comment_on_audio, context=self.get_serializer_context()).data,
                "message": "Commented Succesfully"
            })
        if audio: 
            audio.comments_on_audio.add(comment_on_audio)
            return Response({
                "comment_data": CommentOnAudioSerializer(
                    comment_on_audio, context=self.get_serializer_context()).data,
                "message": "Commented Succesfully"
            })
        return Response({
            "message": "No audio Found"
        })