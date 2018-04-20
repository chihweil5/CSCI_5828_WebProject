from django import forms

from .models import PostNew, Ingredient

class PostForm(forms.ModelForm):

    class Meta:
        model = PostNew
        fields = ('title', 'text',)

class IngredientForm(forms.ModelForm):

    class Meta:
        model = Ingredient
        fields = ('name', 'amount',)
