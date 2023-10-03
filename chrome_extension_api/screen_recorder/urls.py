from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register(r'videos', views.ScreenRecorder, basename='routers')

urlpatterns = [
    # To get all videos and post a video
    path('videos', views.RecordedVideo.as_view(), name='recorded_video'),

    # To get a particular video
    path('video/<int:id>/', views.get_video, name='retrieve_video')
]
