from django.db import models
from django.contrib.auth.models import AbstractUser
from .enums import AUDIO_TYPE


class UserProfile(AbstractUser):
    pass


class CommentOnAudio(models.Model):
    comment_tree = models.ManyToManyField("self", null=True, blank=True)
    comment_text = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    updated_at = models.DateTimeField(auto_now=True, blank=False, null=False)

    class Meta:
        verbose_name_plural = "Audio Comment"

    def __str__(self):
        return "{}".format(self.id)


def audio_folder_upload(instance, filename):
    return (
        f"/audio/{instance.type_of_audio}/{instance.audio_file}"
    )

class AudioTable(models.Model):
    audio_user = models.ForeignKey(UserProfile, on_delete=models.PROTECT)
    audio_file = models.FileField(upload_to=audio_folder_upload)
    type_of_audio = models.CharField(max_length=200, choices=AUDIO_TYPE)
    likes_on_audio = models.IntegerField(blank=True, null=True)
    comments_on_audio = models.ManyToManyField(CommentOnAudio, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    updated_at = models.DateTimeField(auto_now=True, blank=False, null=False)

    class Meta:
        verbose_name_plural = "Audio Table"

    def __str__(self):
        return "{}".format(self.id)

