from django.db.models import Count, Q

from .forms import PostSearchForm
from .models import *

menu = [{'title': "Про сайт", 'url_name': 'about'},
        {'title': "Додати статтю", 'url_name': 'add_page'},
]


class DataMixin:  # миксин для классов представления, в котором мы устанавливаем основной контекст: меню и категории
    paginate_by = 4

    def get_user_context(self, **kwargs):
        context = kwargs
        cats = Category.objects.annotate(Count('blog'))

        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(1)

        context['menu'] = user_menu

        context['cats'] = cats
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context


class SearchMixin:  # миксин для классов представления в которых будет происходить поиск и сортировка
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_published=True)

        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(Q(title__icontains=search_query) | Q(content__icontains=search_query))

        # Обработка сортировки
        sort_option = self.request.GET.get('sort')
        if sort_option == 'latest':
             queryset = queryset.order_by('-time_update')
        elif sort_option == 'oldest':
             queryset = queryset.order_by('time_update')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Обработка поиска
        search_query = self.request.GET.get('search')
        if search_query == None:
            search_query = ""

        if search_query:
            context['search_query'] = search_query

        # Обработка сортировки
        sort_option = self.request.GET.get('sort')
        if sort_option:
            context['sort_option'] = sort_option

        # Предзаполнение формы
        form_initial = {
            'search': search_query,
            'sort': sort_option,
        }
        form = PostSearchForm(initial=form_initial)
        context['form'] = form

        return context