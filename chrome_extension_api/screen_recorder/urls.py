from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register(r'videos', views.ScreenRecorder, basename='routers')

urlpatterns = [
    path('videos', views.RecordedVideo.as_view(), name='recorded_video')
]
