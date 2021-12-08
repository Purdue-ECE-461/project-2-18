from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
# from rest_framework import serializers
# from django.template import loader
# from django.http import HttpResponse
from .models import Package
from .serializers import PackageSerializer, RatingSerializer


class CreatePackage(generics.CreateAPIView):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer


class PackageList(generics.ListAPIView):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer


class PackagebyName(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PackageSerializer
    queryset = Package.objects.all()
    lookup_field = 'name'


class PackageVersion(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PackageSerializer
    queryset = Package.objects.all()
    
    


@api_view(['DELETE'])
def reset(request):
    if(request.method == 'DELETE'):
        Package.objects.all().delete()
        return Response(status=status.HTTP_200_OK)



@api_view(['GET'])
def getRate(request, package):
    pck = Package.objects.get(package=package)
    if pck == None:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'GET':
        # send package through rate packge
        
        x = 1
    serialized_data = RatingSerializer(data={'BusFactor': ratings[0], 'Correctness': ratings[1], 'RampUp': ratings[2],
                                             'ResponsiveMaintainer': ratings[3], 'LicenseScore': ratings[4],
                                             'GoodPinningPractice': ratings[5]})
    serialized_data.is_valid()
    return Response(data=serialized_data.data)


def index(request):
    return render(request, 'index.html')


def input(request):
    return render(request, 'input.html')


def packages(request):
    return render(request, 'packages.html')


# def reset(request):
#     return render(request, 'reset.html')


def authenticate(request):
    return render(request, 'authenticate.html')


'''def dummy(request):
    return  HttpResponseRedirect('/')'''


def button(request):
    return render(request, 'geniusvoice.html')


def output(request):
    output_data = "Genius Voice eliminates friction. For years people have had to learn to interact with computers," \
                  "we turn this around. We teach computers how to interact with humans through voice." \
                  "This creates a seamless experience without losing the human touch."
    website_link = "Visit our website: " + "https://www.geniusvoice.nl/"

    return render(request, "geniusvoice.html", {"output_data": output_data, "website_link": website_link})
