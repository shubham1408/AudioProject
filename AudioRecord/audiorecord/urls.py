from django.urls import path
from knox import views as knox_views
from .views import (LoginAPI, RegisterAPI, AudioTableAPI, LikeAPI, CommentAPI)
from django.urls import path

urlpatterns = [
    path('api/register/', RegisterAPI.as_view(), name='register'),
    path('api/login/', LoginAPI.as_view(), name='login'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('api/audio/', AudioTableAPI.as_view(), name='audio-api'),
    path('api/like/', LikeAPI.as_view(), name='like-api'),
    path('api/comment/', CommentAPI.as_view(), name='comment-api')
] 