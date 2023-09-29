from rest_framework import serializers
from .models import ScreenRecorder


class ScreenRecorderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScreenRecorder
        fields = '__all__'

