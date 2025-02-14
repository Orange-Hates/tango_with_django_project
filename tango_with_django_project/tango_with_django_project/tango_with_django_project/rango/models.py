from django.db import models

from django.db import models
from django.template.defaultfilters import slugify

from django.db import models
from django.template.defaultfilters import slugify
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    # Links UserProfile to a User model instance
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Additional fields
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username

class Category(models.Model):
    # Define max length as a class constant
    NAME_MAX_LENGTH = 128

    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_categories(self):
        return Category.objects.all()


class Page(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title
