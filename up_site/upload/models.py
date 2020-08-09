import os
from urllib import request
from urllib.error import HTTPError
from urllib.parse import unquote

from django.core.files import File
from django.db import models
from django.urls import reverse


class Image(models.Model):
    img_width = models.PositiveIntegerField('Width', null=True, blank=True)
    img_height = models.PositiveIntegerField('Height', null=True, blank=True)
    last_width = models.PositiveIntegerField('LastWidth', null=True, default=0, blank=True)
    last_height = models.PositiveIntegerField('LastHeight', null=True, default=0, blank=True)
    filename = models.CharField('Filename', max_length=100, default='', blank=True)
    image_original = models.ImageField('Image', upload_to='images/',
                                       height_field='img_height', width_field='img_width', blank=True)

    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"

    def __str__(self):
        return self.filename

    def get_absolute_url(self):
        return reverse('upload:image', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        if not (self.pk or self.filename):
            self.filename = unquote(self.image_original.url).split('/')[-1]
        super().save(*args, **kwargs)

    def get_remote_image(self, url):
        if url and not self.image_original:
            try:
                result = request.urlretrieve(url)
            except HTTPError:
                return False
            with open(result[0], 'rb') as f:
                self.image_original.save(
                    os.path.basename(url),
                    File(f)
                )
            self.save()
            return True
