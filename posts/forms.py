from django import forms
from django.forms import ModelForm

from .models import Post


class PostForm(ModelForm):

    class Meta:

        model = Post
        group = forms.CharField(required=False)
        text = forms.CharField(widget=forms.Textarea)
        fields = ("group", "text")
