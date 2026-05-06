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
            'bio': forms.Textarea(attrs={'rows': 3})
        }


class RegisterationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Password',
        'class': 'form-control',
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password'
    }))

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password']

    def clean(self):
        cleaned_data = super(RegisterationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Password does not match!")

    def __init__(self, *args, **kwargs):
        super(RegisterationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Last Name'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Phone Number'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email Address'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class ProfileUpdateForm(forms.ModelForm):
    iimage = forms.ImageField(
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
        fields = ['username', 'email']
