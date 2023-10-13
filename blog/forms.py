from django import forms
from .models import Post
from django.utils import timezone


class PostCreationForm(forms.ModelForm):
    title = forms.CharField(max_length=100)
    content = forms.CharField(widget=forms.Textarea(attrs={"rows":"5"}))
    date_posted = forms.DateTimeField(widget=forms.HiddenInput(),initial=timezone.now)

    class Meta:
        model = Post
        fields = ['title', 'content','date_posted','author']

