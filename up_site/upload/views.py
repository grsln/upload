from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, DetailView
from easy_thumbnails.files import get_thumbnailer

from .forms import ImageForm
from .models import Image


class IndexView(ListView):
    model = Image
    template_name = 'upload/index.html'
    fields = ['filename']


def add_image(request):
    form = ImageForm()
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            if ('image_original' in request.FILES) and (request.POST.get('image_url')):
                return render(request, 'upload/add_image.html',
                              {'error_message': 'Ошибка: выберите файл одним способом.'})
            else:
                if 'image_original' in request.FILES:
                    image = form.save(commit=True)
                else:
                    if request.POST['image_url']:
                        file_url = request.POST['image_url']
                        validate = URLValidator()
                        try:
                            validate(file_url)
                        except ValidationError as e:
                            return render(request, 'upload/add_image.html',
                                          {'error_message': 'Ошибка: неправильная ссылка.'})
                        image = Image()
                        image.filename = file_url.split('/')[-1]
                        if not image.get_remote_image(file_url):
                            return render(request, 'upload/add_image.html',
                                          {'error_message': 'Ошибка открытия ссылки.'})
                    else:
                        return render(request, 'upload/add_image.html',
                                      {'error_message': 'Ошибка: не выбран файл.'})
                return HttpResponseRedirect(reverse('upload:image', args=(image.id,)))
    return render(request, 'upload/add_image.html', {'form': form})


class ImageView(DetailView):
    model = Image
    template_name = 'upload/image.html'

    def post(self, request, *args, **kwargs):
        if request.POST.get('image_width') and request.POST.get('image_height'):
            self.object = self.get_object()
            context = self.get_context_data(object=self.object)
            width = int(request.POST['image_width'])
            height = int(request.POST['image_height'])
            ratio = float(self.object.img_width / self.object.img_height)
            if (width == self.object.last_width) or (height == self.object.last_height):
                if (height == self.object.last_height) and (self.object.last_width != width):
                    height = int(width / ratio)
                else:
                    if (width == self.object.last_width) and (self.object.last_height != height):
                        width = int(height * ratio)
            else:
                width = int(height * ratio) if height < width else width
                height = int(width / ratio) if height > width else height

            options = {'size': (width, height), 'crop': True}
            thumb_url = get_thumbnailer(self.object.image_original).get_thumbnail(options).url
            self.object.last_width = width
            self.object.last_height = height
            self.object.save()
            context['width'] = width
            context['height'] = height
            context['image_url'] = thumb_url
            return render(request, template_name=self.template_name, context=context)
        return render(request, template_name=self.template_name)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        context['width'] = self.object.img_width
        context['height'] = self.object.img_height
        context['image_url'] = self.object.image_original.url
        return render(request, template_name=self.template_name, context=context)
