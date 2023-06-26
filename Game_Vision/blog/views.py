from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView

from .forms import *
from .models import *
from .utils import DataMixin, SearchMixin


class BlogHome(SearchMixin, DataMixin, ListView):  # Класс представления основной страницы
    model = Blog
    template_name = 'blog/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Головна сторінка")
        return dict(list(context.items()) + list(c_def.items()))


class AddPage(DataMixin, LoginRequiredMixin, CreateView):  # Класс представления страницы создания нового поста
    form_class = AddPostForm
    template_name = 'blog/addpage.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Додавання статті")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class About(DataMixin, ListView):  # Класс представления страницы об сайте
    paginate_by = 0
    model = Blog
    template_name = 'blog/about.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Про сайт')
        return dict(list(context.items()) + list(c_def.items()))


class ShowPost(DataMixin, DetailView, FormView):  # Класс представления страницы поста
    model = Blog
    template_name = 'blog/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    form_class = CommentForm

    def get_success_url(self):
        blog = self.get_object()  # Получить текущий объект поста
        return reverse_lazy('post', kwargs={'post_slug': blog.slug})

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context["post"])

        # Получение списка комментариев для текущего поста
        post = self.get_object()
        comments = Comment.objects.filter(blog=post)

        context['comments'] = comments  # Передача списка комментариев в контекст

        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        blog = self.get_object()
        author = User.objects.get(username=self.request.user.username)
        comment = Comment(text=form.cleaned_data['text'], blog=blog, author=author)
        comment.save()
        return super().form_valid(form)


class BlogCategory(SearchMixin, DataMixin, ListView):  # Класс представления для отображения постов по категориям
    model = Blog
    template_name = 'blog/index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = super().get_queryset()
        cat_queryset = queryset.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')
        return cat_queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if context["posts"]:
            c_def = self.get_user_context(title="Категорія - " + str(context["posts"][0].cat),
                                          cat_selected=context["posts"][0].cat_id)
        else:
            c_def = self.get_user_context(title="Пошук по категорії")

        return dict(list(context.items()) + list(c_def.items()))


class RegisterUser(DataMixin, CreateView):  # Класс представления страницы регистрации
    form_class = RegisterUserForm
    template_name = 'blog/register.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Реєстрація")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):  # Класс представления страницы авторизации
    form_class = LoginUserForm
    template_name = 'blog/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизація")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')


class UserProfile(DataMixin, LoginRequiredMixin, LoginView):  # Класс представления страницы профиля пользователя
    model = Blog
    template_name = 'blog/profile.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Про сайт')
        return dict(list(context.items()) + list(c_def.items()))


class UserPostListView(DataMixin, SearchMixin, LoginRequiredMixin, ListView):  # Класс представления страницы с постами пользователя
    model = Blog
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Пости користувача')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        queryset = super().get_queryset()
        cat_queryset = queryset.filter(user=self.request.user, is_published=True)
        return cat_queryset


class EditPostView(DataMixin, LoginRequiredMixin, UpdateView):  # Класс представления страницы для редактирования поста
    model = Blog
    form_class = UpdatePostForm
    template_name = 'blog/edit_post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Редагування посту')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


class DeletePostView(DataMixin, LoginRequiredMixin, DeleteView):  # Класс представления страницы для удаления поста
    model = Blog
    template_name = 'blog/delete_post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Видалення посту')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)