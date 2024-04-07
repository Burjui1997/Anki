from django.urls import path
from . import views
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('catalog/', cache_page(60 * 15)(views.CatalogView.as_view()), name='catalog'),
    path('categories/', views.get_categories, name='categories'),
    path('categories/<slug:slug>/', views.get_cards_by_category, name='category'),
    path('tags/<int:tag_id>/', views.get_cards_by_tag, name='get_cards_by_tag'),
    path('<int:pk>/detail/', views.CardDetailView.as_view(), name='detail_card_by_id'),
    path('add/', views.add_card, name='add_card'),
]
