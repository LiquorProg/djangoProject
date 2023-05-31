from django.shortcuts import render, redirect

from .forms import AddPostForm
from .models import *


menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
]

def index(request):
    posts = Blog.objects.all()

    context = {
        'posts': posts,
        'menu': menu,
        'title': 'Главная страница',
        'cat_selected': 0,
    }
    return render(request, 'blog/index.html', context=context)

def addpage(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            #print(form.cleaned_data)
            form.save()
            return redirect('home')
    else:
        form = AddPostForm()
    return render(request, 'blog/addpage.html', {'form': form, 'menu': menu, 'title': 'Добавление статьи'})

def contact(request):

    context = {
        'menu': menu,
        'title': 'Обратная связь',
    }
    return render(request, 'blog/contact.html', context=context)

def about(request):

    context = {
        'menu': menu,
        'title': 'Обратная связь',
    }
    return render(request, 'blog/about.html', context=context)

def show_post(request, post_slug):
    post = Blog.objects.filter(slug=post_slug)

    context = {
        'post': post[0],
        'menu': menu,
        'title': 'Пост',
    }
    return render(request, 'blog/post.html', context=context)

def blog_category(request, cat_slug):
    posts = Blog.objects.filter(cat__slug=cat_slug)
    cat_id = Category.objects.filter(slug=cat_slug)[0].pk

    print(cat_id)

    context = {
        'posts': posts,
        'menu': menu,
        'title': 'Категория',
        'cat_selected': cat_id,
    }
    return render(request, 'blog/index.html', context=context)