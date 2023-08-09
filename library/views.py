from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse
from .models import User

def index(request):
    
    return HttpResponse("Hello, world.")

def register_user(request):
    return render(request, "user_reg/user_reg.html")