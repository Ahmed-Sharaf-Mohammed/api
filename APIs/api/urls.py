# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_file),
    path('get/<str:user_id>/', views.get_all_data),
    path('image/<str:user_id>/', views.get_images),
    path('link/<str:user_id>/', views.get_links),
    path('time/<str:user_id>/', views.get_times),
    path('image/<str:file_id>/', views.get_image),
]
