from django import forms
from .models import Subscribers


class SubscribeForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'id': 'inputEmail'}))

    class Meta:
        model = Subscribers
        fields = ('email',)
