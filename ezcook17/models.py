from django.db import models
from django.utils import timezone

# import uuid
# from cassandra.cqlengine import columns
# from django_cassandra_engine.models import DjangoCassandraModel

# class Recipe(DjangoCassandraModel):
#     Rid = columns.UUID(primary_key=True, default=uuid.uuid4)
#     content = columns.Integer(index=True)
#     post_time = columns.DateTime()
#     title = colums.Text(required=False)
#     owner = colums.Text(required=False)
#     content = columns.Text(required=False)

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True)
    photo = models.URLField(blank=True)
    location = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class PostNew(models.Model):
    #author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


