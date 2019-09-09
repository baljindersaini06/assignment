from django import forms
from myapp.models import User
from django.forms import ModelForm
from django.contrib.auth.forms import PasswordChangeForm, UserChangeForm



class SignUpForm(forms.ModelForm):
    username = forms.CharField(max_length=254)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254,required=True)
    i_agree=forms.BooleanField(required=True,label='I accept the terms and conditions')
    
   
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name','phone_no', 'email','i_agree')
        

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).count() > 0:
            raise forms.ValidationError('This email address is already registered.')
        return email

    def clean_phone_no(self):
        phone_no = self.cleaned_data.get('phone_no')
        # username = self.cleaned_data.get('username')
        if phone_no and User.objects.filter(phone_no=phone_no).count() > 0:
            raise forms.ValidationError('This phone number is already registered.')
        return phone_no


class SetPasswordForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput,max_length=30, required=False)
    confirm_password = forms.CharField(widget=forms.PasswordInput,max_length=30, required=False)
  
   
    class Meta:
        model = User
        fields = ('password', 'confirm_password')


class PasswordChangedForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'size': '40','padding': '10px 15px','border-radius': '4px','height':'50px'}),label="Old Password")
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'size': '40'}),label="New Password")
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'size': '40','color':'red'}),label="Confirm New Password")


class UserForm(forms.ModelForm):
    profile_image = forms.ImageField(required=False)
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'phone_no', 'profile_image', 'organization', 'address']


class UserChangedForm(UserChangeForm):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    phone_no = forms.IntegerField(required=False)
    profile_image = forms.ImageField(required=False)
    organization = forms.CharField(required=False)
    address = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'phone_no', 'profile_image', 'organization', 'address']

