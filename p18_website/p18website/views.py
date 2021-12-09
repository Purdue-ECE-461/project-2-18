from django.shortcuts import render
from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
# from rest_framework import serializers
# from django.template import loader
# from django.http import HttpResponse
from .models import Package
from .serializers import PackageSerializer, RatingSerializer, UserSerializer
from django.contrib.auth.models import User
from .ranking_modules.url import URL


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CreatePackage(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Package.objects.all()
    serializer_class = PackageSerializer


class PackageList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PackagebyName(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PackageSerializer
    queryset = Package.objects.all()
    lookup_field = 'name'


class PackageVersion(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PackageSerializer
    queryset = Package.objects.all()


@api_view(['DELETE'])
def reset(request):
    if(request.method == 'DELETE'):
        Package.objects.all().delete()
        return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
def getRate(request, pk):
    pck = Package.objects.get(pk=pk)
    if pck == None:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'GET':
        url_idx = pck.url
        url_data = URL()
        url_data.url = url_idx
        if 'npmjs.com' in url_idx:
            url_data.convert_npm_to_github()

        url_data.set_owner()
        # Check for valid repo
        if url_data.owner == -1:
            url_data.net_score = -1
        url_data.set_repo()
        # Check for valid repo
        if url_data.repo == -1:
            url_data.net_score = -1
        url_data.get_bus_factor()
        url_data.get_responsiveness()
        url_data.get_ramp_up()
        url_data.get_correctness()
        url_data.get_license()
        url_data.get_dependecy_score()
        url_data.get_net_score()
    if(url_data.is_ingestible()):
        serialized_data = RatingSerializer(data={'BusFactor': url_data.bus_factor, 'Correctness': url_data.correctness, 'RampUp': url_data.ramp_up,
                                             'ResponsiveMaintainer': url_data.response, 'LicenseScore': url_data.license,
                                             'GoodPinningPractice': url_data.dependency})
        serialized_data.is_valid()
        return Response(data=serialized_data.data)
    else:
        
        return Response(status=status.HTTP_500)


def index(request):
    return render(request, 'index.html')


def packages(request):
    return render(request, 'packages.html')
