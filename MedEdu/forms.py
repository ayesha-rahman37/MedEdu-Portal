from django import forms
from .models import User, Book


class SignupForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User

        fields = [
            "username",
            "email",
            "phone",
            "role",
            "password"
        ]


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'isbn', 'publisher', 'edition', 'year', 
                  'category', 'total_copies', 'available_copies', 'location', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }