# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, redirect
import mysql.connector as sql
from django.http import QueryDict
import requests
import urllib.request 
from PIL import Image 
from task.models import UserImage
from django.contrib.auth import authenticate,login as auth_login
from django.contrib.auth.models import User

email = ''
username = ''
password = ''
image = ''
# user_images = ''


def signup(req):
    global email, username, password
    error_message = ""
    message = "" 

    if req.method == "POST":
        m = sql.connect(host="localhost", user='root', password='root', database='db')
        cursor = m.cursor()
        d = req.POST

        # Extracting data from the request
        for key, value in d.items():
            if key == "email":
                email = value
            if key == "username":
                username = value
            if key == "password":
                password = value

        # Check if the email already exists in the database
        check_email_query = f"SELECT * FROM signup WHERE email = {repr(email)}"
        cursor.execute(check_email_query)
        existing_user = cursor.fetchone()

        if existing_user:
            error_message = "Email is already registered. Try with a different email."
        else:
            # Insert a new record if the email doesn't exist
            message = "Account created successfully."
            insert_query = f"INSERT INTO signup VALUES ({repr(email)}, {repr(username)}, {repr(password)})"
            cursor.execute(insert_query)
            m.commit()
            return redirect('login/')

    return render(req, "signup.html", {"error_message": error_message, "message": message})



def login(req):
    global email, password
    if req.method == "POST":
        m = sql.connect(host="localhost", user='root', password='root', database='db')
        cursor = m.cursor()
        d = req.POST
        for key, value in d.items():
            if key == "email":
                email = value
            if key == "password":
                password = value
        
        # # Debug statements
        # print("Email:", email)
        # print("Password:", password)

        # Using parameterized query to prevent SQL injection
        c = "SELECT * FROM signup WHERE email=%s AND password=%s"
        # print("SQL Query:", c)

        cursor.execute(c, (email, password))
        t = tuple(cursor.fetchall())
        if t == ():
            return render(req, 'error.html')
        else:
            req.session['email'] = email
            return redirect('home/')
        
    return render(req, "login.html")


# def home(req):
#     global image
#     if req.method == "POST":
#         p = req.POST
#         query_dict = p
#         image_file = query_dict.get('imageFile')
#         image_type = query_dict.get('imageType')
#         a = image_file.split(".")
        
#         if a[-1] not in ["jpg", "gif", "png"]:
#             return render(req, "invalid_image.html")

#         if image_type == "portrait":
#             link = "https://chart.googleapis.com/chart?chs=300x300&cht=qr&chl={}&choe=UTF-8".format(image_file)

#             context = {'image_url': link}
#             return redirect('gallary/')
#             return render(req, 'gallary.html', context)

#         elif image_type == "landscape":
#             link = "https://chart.googleapis.com/chart?chs=600x300&cht=qr&chl={}&choe=UTF-8".format(image_file)

#             context = {'image_url': link}
#             return redirect('gallary/')
#     # return redirect('home/')
#     return render(req, "home.html")


def home(req):
    global image
    if req.method == "POST":
        p = req.POST
        query_dict = p
        image_file = query_dict.get('imageFile')
        image_type = query_dict.get('imageType')
        a = image_file.split(".")
        
        if a[-1] not in ["jpg", "gif", "png"]:
            return render(req, "invalid_image.html")
        
        # Get email from the session
        email = req.session.get('email', None)
        
        if req.method == "POST":
            m = sql.connect(host="localhost", user='root', password='root', database='db')
            cursor = m.cursor()
            d = req.POST

            if image_type == "portrait":
                link = "https://chart.googleapis.com/chart?chs=300x300&cht=qr&chl={}&choe=UTF-8".format(image_file)

                insert_img = f"INSERT INTO img VALUES ({repr(link)}, {repr(email)})"
                cursor.execute(insert_img)
                m.commit()

                return redirect('gallary/')
            
            elif image_type == "landscape":
                link = "https://chart.googleapis.com/chart?chs=600x300&cht=qr&chl={}&choe=UTF-8".format(image_file)

                insert_img = f"INSERT INTO img VALUES ({repr(link)}, {repr(email)})"
                cursor.execute(insert_img)
                m.commit()

            return redirect('gallary/')
    
    return render(req, "home.html")


def gallary(req):

    if req.method == "GET":
        m = sql.connect(host="localhost", user='root', password='root', database='db')
        cursor = m.cursor()

        # Get email from the session
        email = req.session.get('email', None)
        print("aaaaaaaaaaaaaa",email)

        # Execute a raw SQL query to fetch images associated with the user's email
        query = f"SELECT image FROM img WHERE forKey = '{email}'"
        cursor.execute(query)
        user_images = cursor.fetchall()
        
        # Reverse the order of user_images
        reversed_user_images = reversed(user_images)

        return render(req, "gallary.html", {"user_images": reversed_user_images})

    # Handle the case where req.method is not POST
    return render(req, "invalid_image.html")
