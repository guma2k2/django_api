from django.db import models

# Create your models here.
class Sentiment(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.CharField(max_length=100)
    sentiment=models.CharField(max_length=50)