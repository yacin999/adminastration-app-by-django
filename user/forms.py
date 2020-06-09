from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.ModelForm):
    username = forms.CharField(max_length=30)
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    password1 = forms.CharField(widget=forms.PasswordInput, min_length=8)
    password2 = forms.CharField(widget=forms.PasswordInput, min_length=8)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name',
                  'last_name', 'password1', 'password2']



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
