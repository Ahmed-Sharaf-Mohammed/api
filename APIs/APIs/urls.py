"""
URL configuration for APIs project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib import admin
from django.urls import path, include  # ← ضروري لـ include
from django.conf import settings       # ← عشان نستخدم settings.MEDIA_URL
from django.conf.urls.static import static  # ← عشان static()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),  # ← اربط تطبيقك هنا (اسمه "api" زي ما قلت)
]

# إضافة دعم عرض ملفات الميديا
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
