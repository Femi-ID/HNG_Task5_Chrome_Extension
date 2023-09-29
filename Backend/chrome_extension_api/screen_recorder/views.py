from django.shortcuts import render
from .models import ScreenRecorder
from .serializers import ScreenRecorderSerializer
from rest_framework.views import APIView
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser


class RecordedVideo(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        """Retrieve a list of all recorded videos."""
        queryset = ScreenRecorder.objects.all()
        serializer = ScreenRecorderSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        """Create/save a recorded video."""
        serializer = ScreenRecorderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecordVideo(viewsets.ViewSet):
    parser_classes = [MultiPartParser, FormParser]

    """A simple viewset for listing all videos."""
    def list(self, request):
        queryset = ScreenRecorder.objects.all()
        serializer = ScreenRecorderSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        video_uploaded = request.FILES.get('video_file')
        content_type = video_uploaded.content_type
        return Response()

