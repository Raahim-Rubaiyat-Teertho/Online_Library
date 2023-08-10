from django.shortcuts import render
from .models import User 
# Create your views here.
from django.http import HttpResponse
from .models import User
from django.db import connection

def index(request):
    return render(request, 'start_page/index.html')

def register_user(request):
    try:
        if(request.method == "GET"):
            fname = request.GET['firstname']
            lname = request.GET['lastname']
            email = request.GET['email']
            password = request.GET['password']
            nid = request.GET['nid']
            phone = request.GET['phone_number']
            address = request.GET['address']
            age = request.GET['age']

        with connection.cursor() as cursor:
            cursor.execute("insert into user (fname, lname, email, password, nid, phone, address, age) values (%s, %s, %s, %s, %s, %s, %s, %s);", [fname, lname, email, password, nid, phone, address, age])
            cursor.execute("insert into rent_provider (user_id) values (%s);", [nid])
            cursor.execute("insert into rent_taker (user_id) values (%s);", [nid])

        return render(request, 'user_reg/dashboard.html')
    except:
        return render(request, "user_reg/user_reg.html")

def user_dashboard(request):
    return render(request, "user_reg/dashboard.html")
