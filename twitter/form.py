from typing import Any
from django import forms
from .models import Meep, Profile

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Profile form

class ProfilePicForm(forms.ModelForm):

    profile_image = forms.ImageField(label="Profile Picture")

    profile_bio = forms.CharField(label="", widget=forms.widgets.Textarea(attrs={"placeholder":"Profile Bio","class":"form-control"}),)
    homepage_link = forms.CharField(label="", widget=forms.widgets.TextInput(attrs={"placeholder":"Home page Link","class":"form-control"}),)
    instagram_link = forms.CharField(label="", widget=forms.widgets.TextInput(attrs={"placeholder":"Instagram Link","class":"form-control"}),)
    facebook_link = forms.CharField(label="", widget=forms.widgets.TextInput(attrs={"placeholder":"FaceBook Link","class":"form-control"}),)
    linkedin_link = forms.CharField(label="", widget=forms.widgets.TextInput(attrs={"placeholder":"Linkin Link","class":"form-control"}),)
    
    class Meta:
        model = Profile
        fields = ('profile_image', 'profile_bio', 'homepage_link', 'instagram_link', 'facebook_link', 'linkedin_link' )


class MeepForm(forms.ModelForm):
    body = forms.CharField(required=True, 
                           widget=forms.widgets.Textarea(
                               attrs={
                                   "placeholder":"Post Your Tweets",
                                   "class":"form-control"
                               }
                           ),
                           label="",
                           )
    class Meta:
        model = Meep
        fields = ('body',)


class SignUp(UserCreationForm):

    email = forms.EmailField( label='', widget=forms.widgets.EmailInput(attrs={'class':'form-control', 'placeholder':'Enter your email'}))
    first_name = forms.CharField(label='',widget=forms.widgets.TextInput(attrs={'class':'form-control', 'placeholder':'Enter your First name'}))
    last_name = forms.CharField(label='',widget=forms.widgets.TextInput(attrs={'class':'form-control', 'placeholder':'Enter your Last name'}))
    

    class Meta:
        model = User
        fields = ['username', 'email','first_name', 'last_name', 'password1', 'password2']


    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(SignUp,self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control' 
        self.fields['username'].widget.attrs['placeholder'] = 'Enter your User Name' 
        self.fields['username'].label = '' 


        self.fields['password1'].widget.attrs['class'] = 'form-control' 
        self.fields['password1'].widget.attrs['placeholder'] = 'Enter your password' 
        self.fields['password1'].label = '' 


        self.fields['password2'].widget.attrs['class'] = 'form-control' 
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm password' 
        self.fields['password2'].label = '' 
