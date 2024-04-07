"""
get_all_cards - возвращает все карточки для представления в каталоге
get_categories - возвращает все категории для представления в каталоге
get_cards_by_category - возвращает карточки по категории для представления в каталоге
get_cards_by_tag - возвращает карточки по тегу для представления в каталоге
get_detail_card_by_id - возвращает детальную информацию по карточке для представления
"""
from django.db.models import F, Q
from django.http import HttpResponse
from django.shortcuts import render
from .models import Card
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import cache_page
from django.http import HttpResponseRedirect
from .forms import CardModelForm
from django.core.paginator import Paginator
# Create your views here.

info = {
    'users_info': 100500,
    'cards_count': 200600,
    'menu': [
        {'title': 'Главная',
         'url_name': 'index'},
        {'title': 'О проекте',
         'url_name': 'about'},
        {'title': 'Каталог',
         'url_name': 'catalog'}
    ],
}

def index(request):
    return render(request, 'main.html', context=info)

def about (request):
    return render(request, 'about.html', context=info)

def catalog(request):
    # Считываем параметры из GET запроса
    sort = request.GET.get('sort', 'upload_date')  # по умолчанию сортируем по дате загрузки
    order = request.GET.get('order', 'desc') # по умолчанию используем убывающий порядок
    search_query = request.GET.get('search_query', '')
    page_number = request.GET.get('page', 1)

    # Сопоставляем параметр сортировки с полями модели
    valid_sort_fields = {'upload_date', 'views', 'favorites'}
    if sort not in valid_sort_fields:
        sort = 'upload_date'  # Возвращаемся к сортировке по умолчанию, если передан неверный ключ сортировки

    # Обрабатываем порядок сортировки
    if order == 'asc':
        order_by = sort
    else:
        order_by = f'-{sort}'

    if not search_query:
        # Получаем отсортированные карточки через жадную загрузку
        cards = Card.objects.prefetch_related('tags').order_by(order_by)

    else:
        cards = Card.objects.prefetch_related('tags').filter(Q(question__icontains=search_query) | Q(answer__icontains=search_query) | Q(tags__name__icontains=search_query)).order_by(order_by).distinct()

    paginator = Paginator(cards, per_page=30)
    page_obj = paginator.get_page(page_number)

    # Подготавливаем контекст и отображаем шаблон
    context = {
        'cards': page_obj,
        'cards_count': len(cards),
        'sort': sort,
        'order': order,
        'menu': info['menu'],
        'page_obj': page_obj
    }
    return render(request, 'cards/catalog.html', context=context)


def get_categories(request):
    return render(request, 'base.html', context=info)

def get_cards_by_category(request, slug):
    return HttpResponse(f'Cards by category {slug}')

def get_cards_by_tag(request, tag_id):
    cards = Card.objects.filter(tags=tag_id)
    context = {
        'cards': cards,
        'cards_count': cards.count(),
        'menu': info['menu']
    }
    return render(request, 'cards/catalog.html', context)

def get_detail_card_by_id(request, card_id):
    """
        /cards/<int:card_id>/detail/
        Возвращает шаблон cards/templates/cards/card_detail.html с детальной информацией по карточке
        """

    # Добываем карточку из БД через get_object_or_404
    # если карточки с таким id нет, то вернется 404
    # Используем F object для обновления счетчика просмотров (views)

    card_obj = get_object_or_404(Card, pk=card_id)
    card_obj.views = F('views') + 1
    card_obj.save()

    card_obj.refresh_from_db()  # Обновляем данные из БД

    card = {
        "card": card_obj,
        "menu": info["menu"],
    }
    return render(request, 'cards/card_detail.html', card, status=200)

# def add_card(request):
#     if request.method == 'POST':
#         form = CardModelForm(request.POST)
#         if form.is_valid():
#             card_answer = form.cleaned_data["answer"]
#             card_question = form.cleaned_data["question"]
#             card_category = form.cleaned_data["category"]
#
#             if Card.objects.filter(question=card_question).exists() or Card.objects.filter(answer=card_answer).exists:
#                 form.add_error('question', 'Карточка уже существует, не можеть быть добавлена')
#                 context = {
#                     'form': form,
#                     'menu': info['menu'],
#                 }
#                 return render(request, 'cards/add_card.html', context, status=400)
#
#
#             card = Card.objects.create(
#                 question = card_question,
#                 answer = card_answer,
#                 category_id = card_category
#             )
#
#             card_id = card.card_id
#
#             card.save()
#             return HttpResponseRedirect(f'/cards/{card_id}/detail/')
#         else:
#             context = {
#                 'form': form,
#                 'menu': info['menu'],
#             }
#             return render(request, 'cards/add_card.html', context, status=400)
#     else:
#         form = CardModelForm()
#         context = {
#             'form': form,
#             'menu': info['menu'],
#         }
#     return render(request, 'cards/add_card.html', context, status=200)


def add_card(request):
    if request.method == 'POST':
        form = CardModelForm(request.POST)
        if form.is_valid():
            card = form.save()
            return redirect(card.get_absolute_url())
    else:
        form = CardModelForm()

    context = {
        'form': form,
        'menu': info['menu'],
    }

    return render(request, 'cards/add_card.html', context)

