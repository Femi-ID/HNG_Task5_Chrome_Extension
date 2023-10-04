from django.shortcuts import render
from .models import ScreenRecorder, VideoChunks
from .serializers import ScreenRecorderSerializer
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
import uuid
import os
from django.conf import settings
from django.http import StreamingHttpResponse
import tempfile
import mimetypes
from django.core.files.uploadedfile import InMemoryUploadedFile
import base64
from io import BytesIO


def video_iterator(video_path, chunk_size=8192):
    with open(video_path, 'rb') as video:
        while True:
            data = video.read(chunk_size)
            if not data:
                break
            yield data


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
        try:
            if serializer.is_valid():
                video = serializer.validated_data['video_file']
                video_id = str(uuid.uuid4())

                # To set the streaming video's content type
                content_type, encoding = mimetypes.guess_type(video.name)
                response = StreamingHttpResponse(video_iterator(video), content_type=content_type)
                response['Content-Disposition'] = f'inline; filename="{video_id}.mp4"'

                # To save the video file to disk
                video_name = os.path.basename(video.name)
                video_path = os.path.join(settings.MEDIA_ROOT, 'videos', video_name)

                with open(video_path, 'wb') as file:
                    for chunk in video.chunks():
                        file.write(chunk)
                return response
            return Response({"error": f"Unable to serialize video file"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                # return Response(serializer.data, status=status.HTTP_201_CREATED)
                # return Response({'message': 'Chunk received successfully.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"Unable to process video file: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_video(request, session_id):
    try:
        # To get complete video via session_id
        video = ScreenRecorder.objects.get(id=id)
        response = Response(video.video_file, content_type='video/mp4', )

        # Also:(Not compulsory) specify the file name
        response['Content-Disposition'] = f'attachment; filename="{session_id}.mp4"'

        return response

    except ScreenRecorder.DoesNotExist:
        return Response({'message': 'The video requested is not found'}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({"error": f"Unable to process video file: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


