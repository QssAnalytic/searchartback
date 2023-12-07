from django.contrib import admin
from django.urls import path
from . import views
app_name='accounts'

urlpatterns=[
    path('signin/',views.login_api,name='signin'),
    path('register/', views.UserRegistrationView.as_view(), name='register')
    ]
