from django.db import models
from django.utils import timezone

class PostNew(models.Model):
    #author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    def __str__(self):
        return self.title

class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    amount = models.CharField(max_length=200)
