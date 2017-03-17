from django import forms
from .models import Post
from django.contrib.auth.models import User



class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title","content","url_field","embeded_field","tags_field","image","draft","publish"]


