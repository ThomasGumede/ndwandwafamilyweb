from typing import Any, Dict, Mapping, Optional, Type, Union
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (AuthenticationForm, PasswordResetForm,
                                       SetPasswordForm, UserCreationForm)
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList


from accounts.models import Address, NextOfKin, Qualification

User = get_user_model()

class UserLoginForm(AuthenticationForm):
    pass
    
class RegistrationForm(UserCreationForm):
    """
    Registration Form - create new user using username, email and password
    """

    email = forms.EmailField(required=True)

    class Meta(UserCreationForm):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name', 'id_number', 'tel', 'photo', 'biography', 'occupation', 'professional_affiliations')

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email)
        if user.exists():
            raise forms.ValidationError("This email already exists")
        return email
    
    def clean_id_number(self):
        data = self.cleaned_data["id_number"]
        user = User.objects.filter(id_number = data)
        if user.exists():
            raise forms.ValidationError("Id number already exists")
        return data
    

class PwdResetForm(PasswordResetForm):
    """
    Custom password reset form
    """

    email = forms.EmailField(max_length=254, widget=forms.TextInput(
        attrs={'placeholder': 'Email', 'id': 'reset_form_email'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Unfortunatley we can not find this email address')
        if not User.objects.get(email=email).is_active:
            raise forms.ValidationError('Unfortunatley, your email address is not verified')

        return email

class PwdResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(widget=forms.PasswordInput(
            attrs={'placeholder': 'New password', 'id': 'reset_form_newpassword'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(
            attrs={'placeholder': 'Retype-New password', 'id': 'reset_form_newpassword2'}))

class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["photo", "first_name", "last_name", "biography", "occupation", "professional_affiliations"]

class GeneralEditForm(forms.ModelForm):
    """
        Form to edit only username and email
    """
    class Meta:
        model = User
        fields = ["username", "email", "tel", "id_number"]

class AddressForm(forms.ModelForm):
    user_address = forms.UUIDField(required=False)
    class Meta:
        model = Address
        fields = ["address_one", "address_two", "city", "country", "state", "zipcode"]
    
    
class NextOfKinForm(forms.ModelForm):
    class Meta:
        model = NextOfKin
        fields = ['full_name', 'relationship', 'tel']

        # widgets = {
        #     'relationship': forms.DateTimeInput(attrs={"class": "border-0 px-3 py-3 {% if form.relationship.errors %} border-2 border-red-500{% endif %} placeholder-blueGray-300 text-gray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"}),
        #     }

class QualificationForm(forms.ModelForm):
    class Meta:
        model = Qualification
        fields = ['institution', 'name', 'qualification_type', 'year']

        # widgets = {
        #     'qualification_type': forms.DateTimeInput(attrs={"class": "border-0 px-3 py-3 {% if form.qualification_type.errors %} border-2 border-red-500{% endif %} placeholder-blueGray-300 text-gray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"}),
        #     }



