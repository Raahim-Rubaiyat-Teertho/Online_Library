from django.shortcuts import render
from .models import User 
# Create your views here.
from django.http import HttpResponse


def index(request):
    return render(request, 'start_page/index.html')
