from django import forms
from django.forms import ModelForm
from .models import Account, Profile
from django.forms import ImageField, FileInput


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']
        labels = {
            'realname': 'Name'
        }
        widgets = {
            'image': forms.FileInput(),
            'bio': forms.Textarea(attrs={
                'rows': 3,
                'class': 'border p-3 w-full rounded-md'
            })
        }


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Create Password',
            'class': 'border border-gray-300 bg-white text-gray-900 p-3 w-full rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400'
        })
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repeat Password',
            'class': 'border border-gray-300 bg-white text-gray-900 p-3 w-full rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400'
        })
    )

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password']

        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Enter First Name',
                'class': 'border border-gray-300 bg-white text-gray-900 p-3 w-full rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400'
            }),

            'last_name': forms.TextInput(attrs={
                'placeholder': 'Enter Last Name',
                'class': 'border border-gray-300 bg-white text-gray-900 p-3 w-full rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400'
            }),

            'email': forms.EmailInput(attrs={
                'placeholder': 'Enter Email Address',
                'class': 'border border-gray-300 bg-white text-gray-900 p-3 w-full rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400'
            }),

            'phone_number': forms.TextInput(attrs={
                'placeholder': 'Enter Phone Number',
                'class': 'border border-gray-300 bg-white text-gray-900 p-3 w-full rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400'
            }),

            
        }

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Password does not match!")


class ProfileUpdateForm(forms.ModelForm):
    image = forms.ImageField(
        widget=forms.FileInput(),
        required=False
    )

    cover_image = forms.ImageField(
        widget=forms.FileInput(),
        required=False
    )
    
    class Meta:
        model = Profile
        fields = [
            'cover_image' ,
            'image' ,
            'full_name', 
            'bio', 
            'about_me', 
            'phone',
            'gender',
            'relationship',
            'friends_visibility',
            'country', 
            'city', 
            'state', 
            'address', 
            'working_at',
        ]

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['email']
