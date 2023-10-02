from django.shortcuts import render
from .models import ScreenRecorder
from .serializers import ScreenRecorderSerializer
from rest_framework.views import APIView
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
import uuid
import os
import tempfile
from django.core.files.uploadedfile import InMemoryUploadedFile
import base64
from io import BytesIO


class RecordedVideo(APIView):
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get(self, request):
        """Retrieve a list of all recorded videos."""
        queryset = ScreenRecorder.objects.all()
        serializer = ScreenRecorderSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        """Create/save a recorded video."""
        # serializer = ScreenRecorderSerializer(data=request.data)
        try:
            # video_file = serializer.validated_data.get("video_file")
            # video_title = serializer.validated_data.get("video_title")
            # if not video_file:
            #     return Response({"error": "Video file must be provided"}, status=status.HTTP_400_BAD_REQUEST)


            # Create a temporary file to store the video chunks
            # temp_video = tempfile.NamedTemporaryFile(delete=False)
            # temp_video.write(video_chunk)

            # TODO: Tell the FE to send the video in chunks periodically
            video_chunk = request.data.get('video_chunk')
            video_chunk = base64.b64decode(video_chunk)

            temp_video = BytesIO(video_chunk)

            # To check if it is the last chunk
            if 'last_chunk' in request.data and request.data['last_chunk']:
                # Close the temporary file
                # temp_video.close()

                # Create a video object and save to thr database
                video = ScreenRecorder.objects.create()
                video_path = os.path.join(settings.MEDIA_ROOT, video.id + '.mp4')

                with open(video_path, 'ab') as video_file_path:
                    # Append the chunk to the temporary file
                    video_file_path.write(temp_video.read())

                video.video_file = video_file_path
                video.save()

                # Clear the temporary file
                os.remove(temp_video.name)

                serializer = ScreenRecorderSerializer(video)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response({'message': 'Chunk received successfully.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"Unable to process video file: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# Create and save new video record
#                 video = ScreenRecorder.objects.create()
#                 video_id = str(uuid.uuid4())
#
#                 video.video_file.save(video_title, video_file, save=False)
#                 video.save()
