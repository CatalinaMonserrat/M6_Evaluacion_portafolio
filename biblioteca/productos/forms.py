from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class CheckoutForm(forms.Form):
    nombre = forms.CharField(max_length=100)
    email = forms.EmailField()
    direccion = forms.CharField(max_length=200, widget=forms.Textarea(attrs={'rows': 2}))

User = get_user_model()

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")