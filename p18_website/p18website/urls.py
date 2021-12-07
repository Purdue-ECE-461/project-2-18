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
Including another URLconf
    1. Import include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import views
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as authviews
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('input', views.input, name="input"),
    path('packages/', views.CreatePackage.as_view()),
    path('reset', views.reset, name="reset"),
    path('authenticate', authviews.LoginView.as_view(template_name="authenticate.html"), name="authenticate"),
    url(r'^$', views.button),
    url(r'^output', views.output, name="jsonFirestore"),
    path('package/', views.CreatePackage.as_view()),
    path('package/byName/<str:name>/', views.PackagebyName.as_view()),
]

urlpatterns += staticfiles_urlpatterns()
