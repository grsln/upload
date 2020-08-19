from django.test import TestCase
from django.urls import reverse

from .models import Image


def add_image_for_test(url):
    image = Image()
    image.get_remote_image(url)
    return image


class ImageModelTests(TestCase):
    def setUp(self):
        self.example_image_url = 'https://funpick.ru/wp-content/uploads/' \
                                 '2017/11/Ochen-legkie-i-krasivye-1.jpeg'
        self.wrong_image_url = 'https://funpick.ru/wp-content/uploads/' \
                               'Ochen-legkie-i-krasivye-1.jpeg'

    def tearDown(self):
        del self.example_image_url
        del self.wrong_image_url

    def test_get_remote_image(self):
        """
        get_remote_image при отсутствии файла по ссылке возвращает False
        """
        image = Image()
        self.assertIs(image.get_remote_image(self.wrong_image_url), False)
        self.assertIs(image.get_remote_image(self.example_image_url), True)

    def test_save_last_size_image(self):
        """
        save_last_size_image запоминает последние введёные размеры изображения
        """
        image = add_image_for_test(self.example_image_url)
        new_size = {'width': '250', 'height': '300'}
        image.save_last_size_image(new_size)
        self.assertIs((new_size['width'] == image.last_width) and (new_size['height'] == image.last_height), True)
        self.assertIs((new_size['width'] == image.img_width) and (new_size['height'] == image.img_height), False)

    def test_get_absolute_url(self):
        """
        get_absolute_url возвращает url изображения
        """
        image = add_image_for_test(self.example_image_url)
        self.assertIs(image.get_absolute_url() == '/image/1/', True)

    def test_resize_image_with_string(self):
        """
        resize_image возвращает исходные размеры при вводе строки
        """
        image = Image(img_width=600, img_height=500)
        new_size = image.resize_image({'width': 'str', 'height': 'str'})
        self.assertIs((new_size['width'] == image.img_width) and (new_size['height'] == image.img_height), True)

    def test_resize_image_with_negative(self):
        """
        resize_image производит расчет для абсолютного значения
        при вводе отрицательного размера
        """
        image = Image(img_width=600, img_height=500)
        new_size = image.resize_image({'width': '-100', 'height': '-200'})
        self.assertIs(new_size['width'] == 100, True)

    def test_resize_image_with_null(self):
        """
        resize_image возвращает исходные размеры при вводе 0
        """
        image = Image(img_width=600, img_height=500)
        new_size = image.resize_image({'width': '0', 'height': '0'})
        self.assertIs((new_size['width'] == image.img_width) and (new_size['height'] == image.img_height), True)

    def test_resize_image_only_width(self):
        """
        resize_image при изменении только ширины высота вычисляется
        """
        image = add_image_for_test(self.example_image_url)
        new_size = image.resize_image({'width': image.img_width // 2, 'height': image.img_height // 2})
        image.save_last_size_image(new_size)
        new_size = image.resize_image({'width': image.img_width // 5, 'height': image.last_height})
        self.assertIs(new_size['height'] == (image.img_height // 5), True)

    def test_resize_image_only_height(self):
        """
        resize_image при изменении только высоты ширина вычисляется
        """
        image = add_image_for_test(self.example_image_url)
        new_size = image.resize_image({'width': image.img_width // 2, 'height': image.img_height // 2})
        image.save_last_size_image(new_size)
        new_size = image.resize_image({'width': image.last_width, 'height': image.img_height // 5})
        self.assertIs(new_size['width'] == (image.img_width // 5), True)

    def test_save(self):
        """
        save переопределенный метод сохраняет в поле filename имя файла
        перед сохранением объекта
        """
        image = add_image_for_test(self.example_image_url)
        self.assertIs(image.filename == 'Ochen-legkie-i-krasivye-1.jpeg', True)


class IndexViewTests(TestCase):
    def setUp(self):
        self.example_image_url = 'https://funpick.ru/wp-content/uploads/' \
                                 '2017/11/Ochen-legkie-i-krasivye-1.jpeg'
        self.wrong_image_url = 'https://funpick.ru/wp-content/uploads/' \
                               'Ochen-legkie-i-krasivye-1.jpeg'

    def tearDown(self):
        del self.example_image_url
        del self.wrong_image_url

    def test_no_images(self):
        """
        Проверка сообщения об отсутствии изображений
        """
        response = self.client.get(reverse('upload:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Нет доступных изображений")
        self.assertQuerysetEqual(response.context['object_list'], [])

    def test_add_image(self):
        """
        Проверка добавления изображения
        """
        image = add_image_for_test(self.example_image_url)
        response = self.client.get(reverse('upload:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, image.filename)
        self.assertQuerysetEqual(response.context['object_list'], [repr(image)])


class ImageViewTests(TestCase):
    def setUp(self):
        self.example_image_url = 'https://funpick.ru/wp-content/uploads/' \
                                 '2017/11/Ochen-legkie-i-krasivye-1.jpeg'

    def tearDown(self):
        del self.example_image_url

    def test_open_image(self):
        """
        Проверка открытия изображения
        """
        image = add_image_for_test(self.example_image_url)
        response = self.client.get(reverse('upload:image', args=(image.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, image.filename)
        self.assertTemplateUsed(response, 'upload/image.html')

    def test_change_image_size(self):
        """
        Проверка изменения размера изображения
        """

        image = add_image_for_test(self.example_image_url)
        data = {
            'image_width': image.img_width // 2,
            'image_height': image.img_height // 2
        }
        response = self.client.post(reverse('upload:image', args=(image.id,)), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['width'], image.img_width // 2)
        self.assertEqual(response.context['height'], image.img_height // 2)

    def test_image_send_no_data(self):
        """
        Проверка отправки пустых размеров на странице изображения
        """
        image = add_image_for_test(self.example_image_url)
        data = {
            'image_width': '',
            'image_height': ''
        }
        response = self.client.post(reverse('upload:image', args=(image.id,)), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual('width' in response.context, False)
        self.assertEqual('height' in response.context, False)


class AddImageTests(TestCase):
    def setUp(self):
        self.example_image_url = 'https://funpick.ru/wp-content/uploads/' \
                                 '2017/11/Ochen-legkie-i-krasivye-1.jpeg'
        self.wrong_image_url = 'https://funpick.ru/wp-content/uploads/' \
                               'Ochen-legkie-i-krasivye-1.jpeg'

    def tearDown(self):
        del self.example_image_url
        del self.wrong_image_url

    def test_add_image_get_request(self):
        """
        Проверка открытия страницы загрузки изображения
        """
        response = self.client.get(reverse('upload:add_image'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'upload/add_image.html')

    def test_add_without_data(self):
        """
        Проверка отправки без выбора изображения
        """
        response = self.client.post(reverse('upload:add_image'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ошибка: не выбран файл.')

    def test_add_two_image(self):
        """
        Проверка ввывода сообщения об ошибке при выборе двумя способами
        """
        with open('ball.jpg', 'rb') as file4test:
            response = self.client.post(reverse('upload:add_image'), {
                'image_url': self.example_image_url,
                'image_original': file4test
            })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ошибка: выберите файл одним способом.')

    def test_redirect2image(self):
        """
        Проверка перехода на страницу изображения при удачном добавлении
        """
        data = {
            'image_url': self.example_image_url,
        }
        response = self.client.post(reverse('upload:add_image'), data=data)
        self.assertEqual(response.status_code, 302)

    def test_wrong_url(self):
        """
        Проверка ввода некорректной ссылки
        """
        data = {
            'image_url': 'sdfg',
        }
        response = self.client.post(reverse('upload:add_image'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ошибка: неправильная ссылка.')

    def test_save_added_files(self):
        """
        Проверка сохранения выбранного файла
        """
        with open('ball.jpg', 'rb') as file4test:
            response = self.client.post(reverse('upload:add_image'), {
                'image_original': file4test
            })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/image/1/')

    def test_open_wrong_url(self):
        """
        Проверка проверка скачивания по несуществующей ссылке
        """
        data = {
            'image_url': self.wrong_image_url,
        }
        response = self.client.post(reverse('upload:add_image'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ошибка открытия ссылки.')
