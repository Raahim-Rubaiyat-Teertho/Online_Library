from django.shortcuts import render
from .models import User 
# Create your views here.
from django.http import HttpResponse
from .models import User

def index(request):
    return render(request, 'start_page/index.html')

def register_user(request):
    return render(request, "user_reg/user_reg.html")