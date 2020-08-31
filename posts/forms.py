from django import forms
from django.forms import ModelForm

from .models import Post


class PostForm(ModelForm):

    class Meta:

        model = Post
        group = forms.CharField(help_text='Измените группу', required=False)
        text = forms.CharField(label = 'Текст записи', help_text='Отредактируйте текст записи и нажмите "Сохранить"', widget=forms.Textarea)
        fields = ("group", "text")
