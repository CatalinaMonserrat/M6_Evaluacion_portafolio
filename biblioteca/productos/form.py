from django import forms

class CheckoutForm(forms.Form):
    nombre = forms.CharField(max_length=100)
    email = forms.EmailField()
    direccion = forms.CharField(max_length=200, widget=forms.Textarea(attrs={'rows': 2}))