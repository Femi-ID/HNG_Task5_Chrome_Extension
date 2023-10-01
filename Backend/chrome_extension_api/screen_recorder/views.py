from django.shortcuts import render
from .models import ScreenRecorder
from .serializers import ScreenRecorderSerializer
from rest_framework.views import APIView
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
import uuid

class RecordedVideo(APIView):
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get(self, request):
        """Retrieve a list of all recorded videos."""
        queryset = ScreenRecorder.objects.all()
        serializer = ScreenRecorderSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        """Create/save a recorded video."""
        serializer = ScreenRecorderSerializer(data=request.data)
        if serializer.is_valid():
            video_file = serializer.validated_data.get("video_file")
            video_title = serializer.validated_data.get("video_title")
            if not video_file:
                return Response({"error": "Video file must be provided"}, status=status.HTTP_400_BAD_REQUEST)
            try:
                # Create and save new video record
                video = ScreenRecorder.objects.create()
                video_id = str(uuid.uuid4())

                video.video_file.save(video_title, video_file, save=False)
                video.save()
            except Exception as e:
                return Response({"error": f"Unable to process video file: {str(e)}"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



