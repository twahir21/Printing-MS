import os
from click import File

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, FileResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from datetime import datetime
import pyprinter
import mimetypes

# Create your views here.
def Signin(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)

            if (user.password == password):
                request.session['uname'] = username
                return userHome(request)
            else:
                data = {'status': "Incorrect password"}
                return render(request, "Home/Templates/signup.html", context=data)
        except Exception as e:
            data = {'status': "username doesn't exist!"}
            return render(request, "Home/Templates/signup.html", context=data)

    return render(request, "Home/Templates/login.html")

def adminLogin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get('password')
        try:
            admin = Admin.objects.get(username=username)
            if admin.password == password:
                request.session['aname'] = username
                # login(request, admin)
                return adminHome(request)
            else:
                data = {'status': "wrong Credentials"}
                return Signin(request)
        except Exception as e:
            data = {'status': "Admin doesn't exist"}
            return Signup(request)
    return render(request, "Home/Templates/adminLogin.html")


def Signup(request):
    if request.method == 'POST':
        uname = request.POST.get("name")
        email = request.POST.get("email")
        contacts = request.POST.get("contacts")
        password = request.POST.get("password")
        re_password = request.POST.get("re-password")

        if(password == re_password):
            user = User(username=uname, email=email, contacts=contacts, password=password)
            user.save()
            request.session['uname'] = uname
            # login(request, user=user)
            return userHome(request)
        else:
            data = {'status': "passwords didn't match"}
            return render(request, "Home/Templates/signup.html", context=data)

    return render(request, "Home/Templates/signup.html")


def adminSignup(request):
    if request.method == "POST":
        username = request.POST.get("name")
        email = request.POST.get("email")
        contacts = request.POST.get("contacts")
        password = request.POST.get("password")
        re_password = request.POST.get("re-password")

        if password == re_password:
            admin = Admin(username=username, email=email, contacts=contacts, password=password)
            admin.save()
            request.session['aname'] = username
            # login(request, admin)
            return adminHome(request)
        else:
            return render(request, "Home/Templates/signup.html")
    return render(request, "Home/Templates/adminSignup.html")

def forgotPassword(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("npassword")

        try:
            user = User.onjects.get(username=username)
            if(user.username == username):
                user.objects.update(password=password)
                user.save()
            else:
                data = {'status': "email doesn't exist"}
                return render(request, "Home/Templates/forgot.html", context=data)
        except Exception as e:
            data = {'status': "something went wrong!!"}
            return render(request, "Home/Templates/forgot.html")
    return render(request, "Home/Templates/forgot.html")


def userHome(request):
    if 'uname' in request.session:
        user = User.objects.get(username=request.session['uname'])
        docs = Document.objects.all()
        data = {'docs': docs, 'uname': user}

        return render(request, 'Home/Templates/userHome.html', context=data)


def adminHome(request):
    if 'aname' in request.session:
        admin = Admin.objects.get(username=request.session['aname'])
        docs = Document.objects.all()
        # printer = pyprinter.Printer(adminHome(docs))
        data = {'aname': admin, 'docs': docs}
        return render(request, "Home/Templates/adminHome.html", context=data)
    else:
        return render(request, "Home/Tempates/adminHome.html")

    return render(request, "Home/Templates/adminHome.html", context=data)



def sendDocument(request):
    if 'uname' in request.session:
        if request.method == "POST":
            file = request.POST.get("file")
            color = request.POST.get("color")
            number_of_copies = request.POST.get("Page_copies")

            # now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            now = datetime.now()

            try:
                doc = Document.objects.get(file=file)
                data = {'status': "document exists! Resend it?"}
                return sendDocument(request)
            except Exception as e:
                user = User.objects.get(username=request.session['uname'])
                doc = Document(name=user, file=file, document_color=color, number_of_copies=number_of_copies, date=now, user_id=user)
                doc.save()
                request.session['doc_status'] = "Success!!"
                return userHome(request)
            

def view_pdf(request, pk):
    # Retrieve the model instance using the primary key (pk)
    try:
        instance = Document.objects.get(document_id=pk)
    except Document.DoesNotExist:
        # Handle the case where the object with the given pk does not exist
        return render(request, 'Home/Templates/userHome.html', {'message': 'Object not found'})

    # Pass the instance to the template
    return render(request, 'Home/Templates/pdf_template.html', {'instance': instance})


def download_pdf(request, document_id):
    pdf_document = get_object_or_404(Document, document_id=document_id)
    response = FileResponse(pdf_document.file.open('rb'))
    return response


def user_logout(request):
    if 'uname' in request.session:
        del request.session['uname']
        return render(request, "Home/Templates/login.html")
    
    if 'aname' in request.session:
        del request.session['aname']
        return render(request, "Home/Templates/adminLogin.html")