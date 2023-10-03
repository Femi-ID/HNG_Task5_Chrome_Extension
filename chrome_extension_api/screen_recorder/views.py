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
            session_id = request.data.get('session_id')
            if not session_id:
                return Response({'message': 'Session ID is required'}, status=status.HTTP_400_BAD_REQUEST)

            # Retrieve all video chunks for the given session ID
            chunks = VideoChunks.objects.filter(session_id=session_id).order_by('chunk_number')

            # Comfirm all chunks are present
            all_chunks = chunks[0].total_chunks
            if len(chunks) != all_chunks:
                return Response({'message': 'Not all chunks have been uploaded'}, status=status.HTTP_400_BAD_REQUEST)

            # add all video chunks into a complete video
            combined_video = b''
            for chunk in chunks:
                with open(chunk.video_chunk.path, 'rb') as file:
                    combined_video += file.read()

            # Delete individual chunk files
            for chunk in chunks:
                os.remove(chunk.video_chunk.path)
                chunk.delete()

            # Save the complete video to the database
            video = ScreenRecorder(session_id=session_id, video_file=combined_video)
            video.save()

            serializer = ScreenRecorderSerializer(video)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

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


