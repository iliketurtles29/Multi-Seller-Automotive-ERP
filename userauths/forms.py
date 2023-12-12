from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauths.models import User, Profile
from core.models import Vendor

class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Enter Username"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Enter Email"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Enter Password"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Enter Confirm Password"}))

    class Meta:
        model = User
        fields = ['username', 'email']

class VendorRegistrationForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Enter Shop name"}))
    description = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "Enter Shop Description"}))
    image = forms.ImageField()
    class Meta:
        model = Vendor
        fields = ['title', 'image', 'description', 'address', 'contact']

class ProfileForm(forms.ModelForm):
    full_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Enter Full Name", "class": "borderless-input resized-input"}))
    bio = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Bio", "class": "borderless-input resized-input"}))
    phone = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Phone", "class": "borderless-input resized-input"}))


    class Meta:
        model = Profile
        fields = ['full_name', 'image', 'bio', 'phone']


