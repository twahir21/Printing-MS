from django.shortcuts import render
# from .models import User

# Create your views here.
def Signin(request):
    return render(request, "Home/Templates/login.html")

def Signup(request):
    # if request.method == 'POST':
    #     username = request.POST.get('name')
    #     email = request.POST.get("email")
    #     contacts = request.POST.get('contacts')
    #     password = request.POST.get('password')

    #     try:
    #         user = User(username=username, password=password, email=email, phone_number=contacts)
    #         user.save()
    #     except Exception as e:
    #         data = {"user already exists"}
    return render(request, "Home/Templates/signup.html")


def forgotPassword(request):
    return render(request, "Home/Templates/forgot.html")

def userHome(request):
    return render(request, "Home/Templates/print.html")