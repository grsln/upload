import os
from urllib import request
from urllib.error import HTTPError
from urllib.parse import unquote
from django.core.files import File
from django.db import models
from django.urls import reverse


# в last_width, last_height сохраняются последние размеры для определения изменений изображения
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

    # url до изображения для перехода после успешного добавления
    def get_absolute_url(self):
        return reverse('upload:image', kwargs={'pk': self.pk})

    # сохраняем имя изображения перед записью объекта модели Image
    def save(self, *args, **kwargs):
        if not (self.pk or self.filename):
            self.filename = unquote(self.image_original.url).split('/')[-1]
        super().save(*args, **kwargs)

    # сквачиваем изображение, в зависимости от рез-та возвращаем True False
    def get_remote_image(self, url):
        if url and not self.image_original:
            try:
                result = request.urlretrieve(url)
            except HTTPError:
                return False
            self.filename = url.split('/')[-1]
            with open(result[0], 'rb') as f:
                self.image_original.save(
                    os.path.basename(url),
                    File(f)
                )
            self.save()
            return True

    # расчет новых размеров для отображения изображения
    def resize_image(self, old_size):
        try:
            width = abs(int(old_size['width']))
            height = abs(int(old_size['height']))
        except ValueError:
            width = self.img_width
            height = self.img_height
        else:
            if width == 0:
                width = self.img_width
            if height == 0:
                height = self.img_height
            ratio = float(self.img_width / self.img_height)
            if (width == self.last_width) or (height == self.last_height):
                if (height == self.last_height) and (self.last_width != width):
                    height = int(width / ratio)
                else:
                    if (width == self.last_width) and (self.last_height != height):
                        width = int(height * ratio)
            else:
                width = int(height * ratio) if height < width else width
                height = int(width / ratio) if height > width else height
        new_size = {'width': width, 'height': height}
        return new_size

    # сохранение последних размеров
    def save_last_size_image(self, size):
        self.last_width = size['width']
        self.last_height = size['height']
        self.save()
