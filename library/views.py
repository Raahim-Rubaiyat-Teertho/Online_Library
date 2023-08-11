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
        if(request.method == "POST"):
            fname = request.POST['firstname']
            lname = request.POST['lastname']
            email = request.POST['email']
            password = request.POST['password']
            nid = request.POST['nid']
            phone = request.POST['phone_number']
            address = request.POST['address']
            age = request.POST['age']

        with connection.cursor() as cursor:
            cursor.execute("insert into user (fname, lname, email, password, nid, phone, address, age) values (%s, %s, %s, %s, %s, %s, %s, %s);", [fname, lname, email, password, nid, phone, address, age])
            cursor.execute("insert into rent_provider (user_id) values (%s);", [nid])
            cursor.execute("insert into rent_taker (user_id) values (%s);", [nid])

        return render(request, 'user_reg/dashboard.html')
    except:
        return render(request, "user_reg/user_reg.html")
    
def loginUser(request):
    return render(request, "user_reg/login_user.html")

def user_dashboard(request):
    return render(request, "user_reg/dashboard.html")
