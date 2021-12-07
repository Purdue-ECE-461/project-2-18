from rest_framework import serializers

from .models import Package

# from django.contrib.auth.models import User


class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = ['id', 'name', 'version', 'url', 'content', 'JSProgram']


class RatingSerializer(serializers.Serializer):
    BusFactor = serializers.DecimalField(max_digits=3, decimal_places=1)
    Correctness = serializers.DecimalField(max_digits=3, decimal_places=1)
    Rampup = serializers.DecimalField(max_digits=3, decimal_places=1)
    ResponsiveMaintainer = serializers.DecimalField(max_digits=3, decimal_places=1)
    LicenseScore = serializers.DecimalField(max_digits=3, decimal_places=1)
    GoodPinningPractice = serializers.DecimalField(max_digits=3, decimal_places=1)
