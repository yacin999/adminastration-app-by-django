from django import forms
from django.contrib.auth.models import User
from .models import Staff

class RegisterForm(forms.ModelForm):
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={"class": "register-inputs username", "placeholder" : "Nom d'utilisateur"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "register-inputs email", "placeholder" : "email"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "register-inputs password1", "placeholder" : "mot de passe"}), min_length=8)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "register-inputs password2", "placeholder" : "confirmer mot de passe"}), min_length=8)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']



       # def clean_password2(self):
       #      cd = self.cleaned_data
       #      if cd['password1'] != cd['password2']:
       #          raise forms.ValidationError('the passwords are not matched')
       #
       #       return cd['password2']

    # def clean_username(self):
    #     cd = cleaned_data['username']
    #     if User.objects.filter(username=cd).exists():
    #         raise forms.ValidationError('this username is already exists')
    #     return cd['username']


class UserForm(forms.ModelForm):
    password1 = forms.CharField(min_length=8, label="", widget=forms.PasswordInput(attrs={
        "class": "module-input", "placeholder": "password"
        }))
    password2 = forms.CharField(min_length=8, label="", widget=forms.PasswordInput(attrs={
        "class": "module-input", "placeholder": "confirm pass..."
        }))
    class Meta:
        model = User
        fields = [ "email", "username", "first_name", "last_name", "password1", "password2"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "module-input", "placeholder": "username"}), 
            "email": forms.EmailInput(attrs={"class": "module-input", "placeholder": "email", 'id': 'email-user'}),
            "first_name": forms.TextInput(attrs={"class": "module-input", "placeholder": "first name"}),
            "last_name": forms.TextInput(attrs={"class": "module-input", "placeholder": "last name"}),
            "password1": forms.PasswordInput(attrs={"class": "module-input", "placeholder": "password"}),
            "password2": forms.PasswordInput(attrs={"class": "module-input", "placeholder": "confirm pass.."}),
        }


        def clean_password2(self):
            pass1 = self.cleaned_data["password1"]
            pass2 = self.cleaned_data["password2"]

            if (pass1 != pass2):
                raise forms.ValidationError("passwords are not matched, make sure to confirm your password")
            return pass2

        def clean_username(self):
            cd = self.cleaned_data

            exists = Staff.objects.filter(username=cd["username"]).exists()
            if(exists):
                forms.ValidationError("this username exists, try another one")
            
            return cd["username"]



class UpdateUserForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "module-input", "placeholder": "username"}), 
            "email": forms.EmailInput(attrs={"class": "module-input", "placeholder": "email"}),
            "first_name": forms.TextInput(attrs={"class": "module-input", "placeholder": "first name"}),
            "last_name": forms.TextInput(attrs={"class": "module-input", "placeholder": "last name"}),
        }




class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ["permissions"]
        widgets = {
            "permissions": forms.SelectMultiple(attrs={"class": "module-input-unique", "placeholder": "first_name"}),
        }

