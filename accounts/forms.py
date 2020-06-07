# model forms

from django.forms import ModelForm
from .models import Order, Customer
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user']


class OrderForm(ModelForm):
    class Meta:
        model = Order
        # here you can also do a list of strings corresponding to each attribute of the model
        fields = '__all__'


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        # find these keywords in the documentation
        fields = ['username', 'email', 'password1', 'password2']
