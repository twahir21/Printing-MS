from django.shortcuts import render
from .models import *
from datetime import datetime

# Create your views here.
def Signin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)

            if(user.password == password):
                request.session['uname'] = username
                return userHome(request)
            else:
                data = {'status': "Incorrect password"}
                return render(request, "Home/Templates/login.html", context=data)
        except Exception as e:
            data = {'status': "user doesn't exist"}
            return Signup(request)
    return render(request, "Home/Templates/login.html")

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
            data = {'status': "passwords didn't match!"}
            return render(request, "Home/Templates/signup.html", context=data)
    return render(request, "Home/Templates/signup.html")


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
        data = {'name': request.session.get('uname')}
        docs = Document.objects.all()
        user = User.objects.get(username=request.session['uname'])

        if 'doc_status' in request.session:
            data['status'] = request.session['doc_status']

        mdata = {'docs': docs, 'uname': user}
        return render(request, 'Home/Templates/userHome.html', context=mdata)

    else:
        data = {'status': 'You need to login first'}
        return Signin(request)

    return render(request, "Home/Templates/userHome.html")


def adminHome(request):
    return render(request, "Home/Templates/adminHome.html")

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
                doc = Document(name=user, file=file, document_color=color, number_of_copies=number_of_copies, date=now, user_id=user.user_id)
                doc.save()
                request.session['doc_status'] = "Success!!"
                return userHome(request)

def logout(request):
    if 'uname' in request.session:
        del request.session['uname']

    return render(request, "Home/Templates/login.html")