from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=150, unique=True)
    description = models.CharField(max_length=500, blank=True)
    image = models.ImageField(upload_to='images/categories', blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"