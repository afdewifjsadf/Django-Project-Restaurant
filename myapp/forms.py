from django.db.models import fields
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import *
from django import forms
import datetime

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['table_no']


class CustomerOrderForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['First_Name','Last_Name']
    
    def __init__(self, *args, **kwargs):
        super(CustomerOrderForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.First_Name:
            self.fields['First_Name'].widget.attrs['readonly'] = True

        if instance and instance.Last_Name:
            self.fields['Last_Name'].widget.attrs['readonly'] = True

    def clean_sku(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.First_Name:
            return instance.First_Name
        else:
            return self.cleaned_data['First_Name']


class CreateUserForm(UserCreationForm):
        class Meta:
            model = User
            fields = ['username', 'email', 'password1', 'password2']
            
        def clean(self):
            email = self.cleaned_data.get('email')
            if User.objects.filter(email=email).exists():
                    raise ValidationError("Email exists")
            return self.cleaned_data

class CustomerForm(ModelForm):
     class Meta:
            model = Customer
            fields =['First_Name', 'Last_Name']


class UpdateOrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['status','table_no']

class UpdateOrderItem(ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']

        
  


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['First_Name','Last_Name', 'phone']
    
    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.First_Name:
            self.fields['First_Name'].widget.attrs['readonly'] = True

        if instance and instance.Last_Name:
            self.fields['Last_Name'].widget.attrs['readonly'] = True
        
        if instance and instance.phone:
            self.fields['phone'].widget.attrs['readonly'] = True


    def clean_sku(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.First_Name:
            return instance.First_Name
        else:
            return self.cleaned_data['First_Name']

class DateInput(forms.DateInput):
    input_type = 'date'

class BookTableForm(ModelForm):
    class Meta:
        model = BookTable
        fields = ['email', 'date_time', 'timeBook','people', 'message']
        widgets = {
            'date_time': DateInput()
        }
                                                                                                                                                           


class CreateUserForm(UserCreationForm):        
        class Meta:
            model = User
            fields = ['username', 'email', 'password1', 'password2']
            
        def clean(self):
            email = self.cleaned_data.get('email')
            if User.objects.filter(email=email).exists():
                    raise ValidationError("Email exists")
            return self.cleaned_data
    
class UpdateCustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['First_Name','Last_Name', 'phone', 'image']
        

class UpdateUserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

