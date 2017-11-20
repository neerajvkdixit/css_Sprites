from django.db import models


class CssConf(models.Model):
    name = models.CharField(max_length=30)
    imageMap1 = models.TextField()
    imageMap2 = models.TextField()
# Create your models here.
