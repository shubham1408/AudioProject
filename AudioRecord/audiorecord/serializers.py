from rest_framework import serializers
from .models import (UserProfile, CommentOnAudio, AudioTable, LikeOnAudio)


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'username', 'email')


class CommentOnAudioTreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentOnAudio
        fields = '__all__'


# CommentOnAudio Serializer
class CommentOnAudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentOnAudio
        fields = '__all__'

    def create(self, validated_data):
        comment = CommentOnAudio.objects.create( 
            comment_text=validated_data['comment_text'],
            )
        return comment


    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['comment_tree'] = CommentOnAudioTreeSerializer(
            instance=instance.comment_tree.all(), many=True).data
        return response


# LikeOnAudio Serializer
class LikeOnAudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeOnAudio
        fields = '__all__'

    def create(self, validated_data):
        like = LikeOnAudio.objects.create(
            liked_by_user=validated_data['liked_by_user'])
        return like

# AudioTable Serializer
class AudioTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioTable
        fields = '__all__'

    def create(self, validated_data):
        audio = AudioTable.objects.create(
            audio_user=validated_data['audio_user'], 
            audio_file=validated_data['audio_file'],
            type_of_audio=validated_data['type_of_audio'])
        return audio

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['likes_on_audio'] = LikeOnAudioSerializer(
            instance=instance.likes_on_audio.all(), many=True).data
        response['comments_on_audio'] = CommentOnAudioSerializer(
            instance=instance.comments_on_audio.all(), many=True).data
        return response


# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(
            validated_data['username'], validated_data['first_name'], validated_data['last_name'],
            validated_data['email'], validated_data['password'])
        return user