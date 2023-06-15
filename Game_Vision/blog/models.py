from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from slugify import slugify


class Blog(models.Model):
    title = models.CharField(max_length=160, verbose_name="Заголовок")
    slug = models.SlugField(max_length=160, unique=True, db_index=True, verbose_name="URL")
    content = models.TextField(blank=True, verbose_name="Текст статті")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Фото")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Час створення")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Час зміни")
    is_published = models.BooleanField(default=True, verbose_name="Публікація")
    cat = models.ForeignKey("Category", on_delete=models.PROTECT, verbose_name="Категорії")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.slug:  # проверяем, не заполнено ли поле slug
            self.slug = slugify(self.title)  # генерируем slug из поля title
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Категорія")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def save(self, *args, **kwargs):
        if not self.slug:  # проверяем, не заполнено ли поле slug
            self.slug = slugify(self.name)  # генерируем slug из поля title
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})