# from django.db import models
# from django.utils import timezone
#
# class PostNew(models.Model):
#     #author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
#     title = models.CharField(max_length=200)
#     text = models.TextField()
#     def __str__(self):
#         return self.title
#
# class Ingredient(models.Model):
#     name = models.CharField(max_length=200)
#     amount = models.CharField(max_length=200)


import uuid
from cassandra.cqlengine import columns
from django_cassandra_engine.models import DjangoCassandraModel

class UserModel(DjangoCassandraModel):
    class Meta:
        get_pk_field='id'
    id = columns.UUID(primary_key=True)
    lastname = columns.Text(required=False)
    firstname = columns.Text(required=False)
    username = columns.Text(primary_key=True)
    password = columns.Text(required=False)
    admin = columns.Boolean(required=False)
    favorite = columns.Set(columns.UUID(), required=False)
    ingredients = columns.Map(columns.Text(), columns.Float(), required=False)

class RecipeModel(DjangoCassandraModel):
    class Meta:
        get_pk_field='id'
    id = columns.UUID(primary_key=True)
    title = columns.Text()
    content = columns.Text()
    owner = columns.Text()
    ingredients = columns.Map(columns.Text(), columns.Float(), required=False)
    post_time = columns.DateTime(primary_key=True, clustering_order="DESC")

class IngredientModel(DjangoCassandraModel):
    class Meta:
        get_pk_field='id'
    id = columns.UUID(primary_key=True)
    name = columns.Text()
    category  = columns.Text()
    usedby = columns.List(columns.Text)
