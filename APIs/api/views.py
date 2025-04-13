from django.shortcuts import render

# Create your views here.
# views.py
import uuid
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Upload
from .serializers import UploadSerializer
from django.http import FileResponse
from django.shortcuts import get_object_or_404

@api_view(['POST'])
def upload_file(request):
    file = request.FILES.get('file')
    link = request.POST.get('link')
    user_id = request.POST.get('user_id')

    if not file or not link or not user_id:
        return Response({"error": "Missing data"}, status=status.HTTP_400_BAD_REQUEST)

    file_id = f"{uuid.uuid4().hex}_{file.name}"
    upload = Upload.objects.create(
        file_id=file_id,
        filename=file.name,
        link=link,
        user_id=user_id,
        file=file
    )

    return Response({"message": "Uploaded successfully", "id": upload.file_id}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_all_data(request, user_id):
    uploads = Upload.objects.filter(user_id=user_id)
    if not uploads:
        return Response({"error": "No files found for this user"}, status=status.HTTP_404_NOT_FOUND)
    serializer = UploadSerializer(uploads, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_images(request, user_id):
    uploads = Upload.objects.filter(user_id=user_id)
    if not uploads:
        return Response({"error": "No images found"}, status=status.HTTP_404_NOT_FOUND)
    return Response([{"image_url": f"/api/image/{u.file_id}"} for u in uploads])

@api_view(['GET'])
def get_links(request, user_id):
    uploads = Upload.objects.filter(user_id=user_id)
    if not uploads:
        return Response({"error": "No links found"}, status=status.HTTP_404_NOT_FOUND)
    return Response([{"link": u.link} for u in uploads])

@api_view(['GET'])
def get_times(request, user_id):
    uploads = Upload.objects.filter(user_id=user_id)
    if not uploads:
        return Response({"error": "No timestamps found"}, status=status.HTTP_404_NOT_FOUND)
    return Response([{"uploaded_at": u.timestamp.isoformat()} for u in uploads])

@api_view(['GET'])
def get_image(request, file_id):
    upload = get_object_or_404(Upload, file_id=file_id)
    return FileResponse(upload.file)
