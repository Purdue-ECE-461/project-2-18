'''from django.http import HttpResponse
#from django.template import loader'''
from django.shortcuts import render
from rest_framework import generics
from rest_framework import mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response
from p18website.models import Package
from p18website.serializers import PackageSerializer, RatingSerializer

class CreatePackage(generics.ListCreateAPIView):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer


class PackagebyName(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PackageSerializer
    queryset = Package.objects.all()
    lookup_field = 'name'

class PackageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer

def index(request):
    return render(request, 'index.html')


def input(request):
    return render(request, 'input.html')


def packages(request):
    return render(request, 'packages.html')


def reset(request):
    return render(request, 'reset.html')


def authenticate(request):
    return render(request, 'authenticate.html')

'''def dummy(request):
    return  HttpResponseRedirect('/')'''

def button(request):

    return render(request,'geniusvoice.html')

def output(request):
    
    output_data = "Genius Voice eliminates friction. For years people have had to learn to interact with computers, we turn this around. We teach computers how to interact with humans through voice. This creates a seamless experience without losing the human touch."
    website_link = "Visit our website: " + "https://www.geniusvoice.nl/"
    
    return render(request,"geniusvoice.html",{"output_data":output_data, "website_link":website_link})
    