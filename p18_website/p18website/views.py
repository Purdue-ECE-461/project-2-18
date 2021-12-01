'''from django.http import HttpResponse
from django.template import loader'''
from django.shortcuts import render


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
