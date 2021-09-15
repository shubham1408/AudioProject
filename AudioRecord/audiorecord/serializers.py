from rest_framework import serializers
from .models import UserProfile
from .models import CommentOnAudio, AudioTable


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'username', 'email')


# CommentOnAudio Serializer
class CommentOnAudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentOnAudio
        fields = '__all__'

# AudioTable Serializer
class AudioTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioTable
        fields = '__all__'

    def create(self, validated_data):
        # import ipdb; ipdb.set_trace()
        # comment = CommentOnAudio.objects.create(validated_data['comment'])
        audio = AudioTable.objects.create(
            audio_user=validated_data['audio_user'], 
            audio_file=validated_data['audio_file'],
            type_of_audio=validated_data['type_of_audio'],
            likes_on_audio=validated_data['likes_on_audio'])
        return audio


# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
        return user