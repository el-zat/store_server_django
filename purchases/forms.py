from django import forms
from purchases.models import Purchase


class PurchaseForm(forms.ModelForm):
    firstname = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Firstname'}))
    lastname = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Lastname'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'you@example.com'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country, City, Street, House'}))

    class Meta:
        model = Purchase
        fields = ('firstname', 'lastname', 'email', 'address')