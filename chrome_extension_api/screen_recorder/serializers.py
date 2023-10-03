from rest_framework import serializers
from .models import ScreenRecorder, VideoChunks


class ScreenRecorderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScreenRecorder
        fields = '__all__'


class VideoChunkSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoChunks
        fields = '__all__'