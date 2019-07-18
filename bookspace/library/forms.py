from django import forms
from .models import User, Book, UserAndBook



class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'image']


class BookForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = ['author', 'title', 'number_of_pages', 'price']

    description = forms.CharField(widget=forms.Textarea)
    name = forms.CharField(widget=forms.HiddenInput())
