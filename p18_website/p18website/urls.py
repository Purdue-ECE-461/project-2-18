"""p18website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URL conf
    1. Import include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('packages/', views.PackageList.as_view(), name="packages"),
    path('package/<str:pk>/', views.PackageVersion.as_view()),
    path('package/<str:pk>/rate', views.getRate, name = "rate"),
    path('reset/', views.reset, name="reset"),
    path('authenticate/', include('rest_framework.urls')),
    path('package/', views.CreatePackage.as_view()),
    path('package/byName/<str:name>/', views.PackagebyName.as_view()),
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
