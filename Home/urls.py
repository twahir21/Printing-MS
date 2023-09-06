from . import views
from django.urls import include, path

urlpatterns = [
    path('', views.Signin, name="signin"),
    path('signup/', views.Signup, name="signup"),
    path('forgotpassword/', views.forgotPassword, name="forgotpassword"),
    path('userHome/', views.userHome, name="userHome"),
]