from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from .models import *
from datetime import datetime
import pyprinter

# Create your views here.
def Signin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
            if user.password == password:
                request.session['uname'] = username
                return userHome(request)
            # else:
            #
        except Exception as e:
            data = {'status': "user doesn't exist"}
            return Signup(request)

    return render(request, "Home/Templates/login.html")

def adminLogin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get('password')
        try:
            admin = Admin.objects.get(username=username)
            if admin.password == password:
                request.session['aname'] = username
                return adminHome(request)
            else:
                data = {'status': "wrong Credentials"}
                return Signin(request)
        except Exception as e:
            data = {'status': "Admin doesn't exist"}
            return Signup(request)
    return render(request, "Home/Templates/adminLogin.html")


def Signup(request):
    if request.method == "POST":
        username = request.POST.get("name")
        email = request.POST.get("email")
        contacts = request.POST.get("contacts")
        password = request.POST.get("password")
        re_password = request.POST.get("re-password")

        if(password == re_password):
            user = User(username=username,email=email,contacts=contacts,password=password)
            user.save()
            request.session['uname'] = username
            return userHome(request)
        else:
            return render(request, "Home/Templates/signup.html")
    return render(request, "Home/Templates/signup.html")


def adminSignup(request):
    if request.method == "POST":
        username = request.POST.get("name")
        email = request.POST.get("email")
        contacts = request.POST.get("contacts")
        password = request.POST.get("password")
        re_password = request.POST.get("re-password")

        if(password == re_password):
            admin = Admin(username=username,email=email,contacts=contacts,password=password)
            admin.save()
            request.session['aname'] = username
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
        docs = Document.objects.values().all()
        data = {'docs': docs, 'uname': user}
        return render(request, 'Home/Templates/userHome.html', context=data)

        # if 'doc_status' in request.session:
        #     data['status'] = request.session['doc_status']

        # if docs.name == user.username:
        #     user_docs = Document.objects.values('document_color','file','number_of_copies','date').all()
        #     data = {'docs': user_docs, 'uname': user}
        #     return render(request, 'Home/Templates/userHome.html', context=data)
        # else:
        #     data = {'status': 'No document'}
        #     return sendDocument(request)

    else:
        data = {'status': 'You need to login first'}
        return Signin(request)

    return render(request, "Home/Templates/userHome.html")

@login_required
def adminHome(request):
    if 'aname' in request.session:
        admin = Admin.objects.get(username=request.session['aname'])
        docs = Document.objects.values().all()
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

@login_required
def logout(request):
    if 'uname' in request.session:
        del request.session['uname']

    return render(request, "Home/Templates/login.html")