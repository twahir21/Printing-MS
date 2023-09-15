from . import views
from django.urls import include, path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.Signin, name="signin"),
    path('signup/', views.Signup, name="signup"),
    path('forgotpassword/', views.forgotPassword, name="forgotpassword"),
    path('userHome/', views.userHome, name="userHome"),
    path('adminHome', views.adminHome, name="adminHome"),
    path('logout/', views.logout, name="logout"),

    path('sendDocument/', views.sendDocument, name="sendDocument"),
]