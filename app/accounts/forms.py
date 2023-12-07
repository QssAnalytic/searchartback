from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm 
class UserForm(UserCreationForm):
    #password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = CustomUser
        fields = ("first_name","last_name","gender","email","phone_number", 
                  "company","industry","job_title"
                  ) 
