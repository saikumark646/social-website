from django.utils.text import slugify
from django.db import models

# Create your models here.

from django.conf import settings


class Image(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='images_created',
                             on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    slug = models.SlugField(blank=True)
    url = models.URLField()
    image = models.ImageField(upload_to='images/%Y/%m/%d/')
    # title = models.CharField(blank=True) // title can be kept blank. In the database ("") will be stored. null=True blank=True This means that the field is optional in all circumstances.
    description = models.TextField(blank=True)
    created = models.DateField(auto_now_add=True, db_index=True)
    # db_index=True so that Djangocreates an index in the database
    user_like = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='image_liked', blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

        """ 
In the preceding code, you use the slugify() function provided by Django to
automatically generate the image slug for the given title when no slug is provided.
Then, you save the object. By generating slugs automatically, users don't have
to manually enter a slug for each image.

The ManyToManyField fields provide a many-to-many manager that allows you to
retrieve related objects, such as image.users_like.all(), or get them from
a user object, such as user.images_liked.all().
"""
