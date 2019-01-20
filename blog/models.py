from django.conf import settings
from django.db import models
from django.utils import timezone

#id, author, recomendation, stars, content, advantages, disadvantages, useful, unuseful, add_date, purchase_date

class Post(models.Model):
    id = models.IntegerField(primary_key=True)
    author = models.CharField(max_length=50,null=True)
    recomendation = models.CharField(max_length=200,null=True)
    stars = models.CharField(max_length=200,null=True)
    content = models.TextField(null=True)
    product_id = models.IntegerField(default=0,null=True)
    useful = models.IntegerField(null=True)
    unuseful = models.IntegerField(null=True)
    purchase_date = models.DateTimeField(blank=True, null=True)
    add_date = models.DateTimeField(blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    
    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title