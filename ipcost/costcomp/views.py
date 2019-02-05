from django.shortcuts import render
from django.http import HttpResponse

#index route
def index(response):
    return HttpResponse('Hello, world')
