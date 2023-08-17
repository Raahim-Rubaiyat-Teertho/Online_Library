from django.shortcuts import render
from django.shortcuts import redirect
from .models import User, Book, Author 
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from django.http import HttpResponse
from .models import User
from django.db import connection
from sslcommerz_lib import SSLCOMMERZ 

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
    try:
        if(request.method == "POST"):
            email = request.POST['email']
            password = request.POST['pw']

        with connection.cursor() as cursor:
            cursor.execute("select * from user where email = %s and password = %s", [email, password])
            login_dets = cursor.fetchone()

        with connection.cursor() as cursor:
            cursor.execute("select * from book where provider_id = %s", [login_dets[0]])
            user_books = cursor.fetchall()
        
        if(email == login_dets[3] and password == login_dets[4]):
            # return render(request, 'user_reg/dashboard.html', {'data' : l, 'data1':ub})
            # return user_dashboard(request, login_dets, user_books)
            # return Dashboard(login_dets, user_books)
            request.session['user_info'] = login_dets
            request.session['user_books'] = user_books
            return redirect('login_user')
       

        else:
            #messages
            return render(request, "user_reg/login_user.html")
        
    except:
        return render(request, "user_reg/login_user.html")


def user_dashboard(request):
    l = request.session.get('user_info')
    ub = request.session.get('user_books')
    with connection.cursor() as cursor:
        cursor.execute("select book.book_id, name, author_name, genre, publisher, rent_cost from book inner join author where book.book_id = author.book_id and book.provider_id = %s;", [l[0]])
        uub = cursor.fetchall()
    return render(request, 'user_reg/dashboard.html', {'data':l, 'data1':ub, 'data2':uub})

def upload_book(request):
    try:
        user_info = request.session.get('user_info')
        # print(user_info[0])

        if(request.method == "POST"):
            book_name = request.POST['book_name']
            author_name = request.POST['author']
            genre = request.POST['genre']
            copy_no = request.POST['copy_no']
            publisher = request.POST['publisher']
            rent_cost = request.POST['rent_cost']
        

        with connection.cursor() as cursor:
            cursor.execute("insert into book (book_id, name, genre, copy_number, publisher, rent_cost, provider_id) values (%s, %s, %s, %s, %s, %s, %s);", [0, book_name, genre, copy_no, publisher, rent_cost, user_info[0]])
            cursor.execute("select book_id from book where name = %s and provider_id = %s;", [book_name, user_info[0]])
            book_id = cursor.fetchone()
            cursor.execute("insert into author (book_id, author_name) values (%s, %s);", [book_id[0], author_name])
            result = cursor.fetchone()

        if(result == None):
            return redirect('user_dashboard')        

        return render(request, 'user_reg/upload_book_front.html')
    except:
        return render(request, 'user_reg/upload_book_front.html')
    

def search_book(request):
    try:
        if(request.method == "POST"):
            book_n = request.POST['book_name']
        
        user_info = request.session.get('user_info')

        book_n = book_n + '%'
        with connection.cursor() as cursor:
            cursor.execute("select book.book_id, name, genre, copy_number, publisher, book.rent_cost, book.provider_id, user.fname, user.lname, book.book_id, author.author_name from book inner join author inner join rents inner join user where book.book_id = author.book_id and rents.book_id != book.book_id and book.name like %s and user.nid = book.provider_id and book.provider_id != %s;", [book_n, user_info[0]])
            search_result = cursor.fetchall()
            print(search_result)

        names = []
        for i in range(len(search_result)):
            with connection.cursor() as cursor:
                cursor.execute('select fname, lname from user where nid = %s', [search_result[i][6]])
                user_name = cursor.fetchall()
                names.append(user_name)

        # print(names)
        print(user_info)

        request.session['book_details'] = search_result
        print(search_result)

        return render(request, 'user_reg/search_book.html', {"d1":search_result, 'd2' : user_name, 'd3' : names})
    except:

        return render(request, 'user_reg/search_book.html')
    
def confirm_rent(request, pk):
    book_details = request.session.get('book_details')
    print(book_details)

    with connection.cursor() as cursor:
        cursor.execute('select fname, lname from user where nid = %s', [book_details[0][6]])
        user_name = cursor.fetchall()
        print(user_name)

    book = Book.objects.get(book_id=pk)
    author = Author.objects.get(book_id = pk)
    checkout_dets = [book.rent_cost]
    request.session['book_details'] = checkout_dets
    

    return render(request, 'user_reg/confirm_rent.html', {'d1' : book_details, 'd2' : user_name, 'book' : book, 'author' : author})

@csrf_exempt
def payment(request):
    # user_info = request.session.get('user_info')
    # book_details = request.session.get('book_details')

    try:
        user_info = request.session.get('user_info')
        print(user_info)
        book_details = request.session.get('book_details')
        print(book_details)
        settings = { 'store_id': 'onlin64dd360da6a67', 'store_pass': 'onlin64dd360da6a67@ssl', 'issandbox': True }
        sslcz = SSLCOMMERZ(settings)
        post_body = {}
        post_body['total_amount'] = book_details[0]
        post_body['currency'] = "BDT"
        post_body['tran_id'] = "1"
        post_body['success_url'] = "http://127.0.0.1:8000/confirmed_pay/"
        post_body['fail_url'] = "https://www.youtube.com/"
        post_body['cancel_url'] = "https://www.instagram.com/"
        post_body['emi_option'] = 0
        post_body['cus_name'] = user_info[5] + ' ' + user_info[6]
        post_body['cus_email'] = user_info[3]
        post_body['cus_phone'] = user_info[1]
        post_body['cus_add1'] = "customer address"
        post_body['cus_city'] = "Dhaka"
        post_body['cus_country'] = "Bangladesh"
        post_body['shipping_method'] = "NO"
        post_body['multi_card_name'] = ""
        post_body['num_of_item'] = 1
        post_body['product_name'] = "Test"
        post_body['product_category'] = "Test Category"
        post_body['product_profile'] = "general"

        response = sslcz.createSession(post_body) # API response
        print(response)
        return redirect(response['GatewayPageURL'])
    
    except:
        return render(request, 'user_reg/confirm_rent.html')
    
@csrf_exempt
def confirmed(request):
    return render(request, "user_reg/confirmed.html")