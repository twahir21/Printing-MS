from django.shortcuts import render
from .models import User

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
    return render(request, "Home/Templates/userHome.html")

def logout(request):
    return render(request, "Home/Templates/login.html")