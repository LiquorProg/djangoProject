from django.test import TestCase

from django.contrib.auth.models import User

from Game_Vision.settings import BASE_DIR
from .models import Blog, Category
from django.core.files.uploadedfile import SimpleUploadedFile
import os

class BlogPostTest(TestCase):
    def setUp(self):
        # Создаем пользователя
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Создаем категорию
        self.category = Category.objects.create(name='TestCategory')

        # Логинимся как созданный пользователь
        self.client.login(username='testuser', password='testpassword')

    def test_create_blog_post(self):
        # Проверяем, что пользователь залогинен
        self.assertTrue(self.user.is_authenticated)

        # Путь к созданному изображению
        image_path = os.path.join(BASE_DIR, 'media', 'test-photo.jpg')

        # Использование изображения в тестовом запросе
        with open(image_path, 'rb') as f:
            image_file = SimpleUploadedFile('test-photo.jpg', f.read(), content_type='image/jpeg')

        # Создаем пост
        response = self.client.post('/addpage/', {
            'title': 'Test Post',
            'content': 'This is a test post',
            'photo': image_file,
            'cat': self.category.id,
        })

        # Проверяем, что пост был успешно создан и нас перенаправили
        self.assertEqual(response.status_code, 302)

        # Проверяем, что пост был добавлен в базу данных
        post = Blog.objects.filter(title='Test Post').first()
        self.assertIsNotNone(post)

        # Проверяем, что созданный пост имеет правильные значения полей
        self.assertEqual(post.title, 'Test Post')
        self.assertEqual(post.content, 'This is a test post')
        self.assertEqual(post.cat, self.category)
        self.assertEqual(post.user, self.user)