from django import forms
from ckeditor.widgets import CKEditorWidget

from .models import Post, Response


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'category',
            'title',
            'content',
        ]
        widgets = {
            'content': forms.CharField(widget=CKEditorWidget()),
        }


class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = [
            'text',
        ]
