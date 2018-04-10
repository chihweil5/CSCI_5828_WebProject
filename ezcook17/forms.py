from django import forms

from .models import PostNew

class PostForm(forms.ModelForm):

    class Meta:
        model = PostNew
        fields = ('title', 'text',)