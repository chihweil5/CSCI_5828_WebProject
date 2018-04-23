from django import forms
from .models import RecipeModel

class PostForm(forms.ModelForm):

    class Meta:
        model = RecipeModel
        fields = ('title', 'content',)

class IngredientForm(forms.Form):
    name = forms.CharField(label='Ingredient Name', max_length=100)
    amount = forms.CharField(label='Ingredient Amount', max_length=100)
