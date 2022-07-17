from django import forms
from .models import Image
from django.utils.text import slugify
from urllib import request
from django.core.files.base import ContentFile


class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'url', 'description')
        widgets = {
            'url': forms.HiddenInput,
        }

    def clean_url(self):
        # taking submiited image url/ image name(with .jpg , .jpeg extension)
        url = self.cleaned_data['url']
        valid_extentions = ['jpg', 'jpeg']
        extention = url.rsplit('.', 1)[1].lower()
        if extention not in valid_extentions:
            raise forms.ValidationError(
                'the url does not match valid extentions')
        else:
            return url

    def save(self, force_insert=False, force_update=False, commit=True):
        image_url = self.cleaned_data['url']
        extention = image_url.rsplit('.', 1)[1].lower()
        # crearting new image instance with commit =False
        image = super().save(commit=False)
        name = slugify(image.title)  # making slug as title
        image_name = f'{name}.{extention}'   # new image name is created

        # download image from the given URL
        response = request.urlopen(image_url)
        image.image.save(image_name, ContentFile(response.read()), save=False)
        # save=False parameterto avoid saving the object to the database yet.
        if commit:
            image.save()
        return image

   # In order to maintain the same behavior as the save() method you override, you save the form to the database only when the commit parameter is True.
"""
Overriding the save() method of a ModelForm
As you know, ModelForm provides a save() method to save the current model
instance to the database and return the object. This method receives a Boolean
commit parameter, which allows you to specify whether the object has to be persisted
to the database. If commit is False, the save() method will return a model instance
but will not save it to the database. You will override the save() method of your
form in order to retrieve the given image and save it. 
"""
