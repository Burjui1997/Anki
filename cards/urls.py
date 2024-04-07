from django.urls import path
from . import views

urlpatterns = [
    path('catalog/', views.catalog, name='catalog'),
    path('categories/', views.get_categories, name='categories'),
    path('categories/<slug:slug>/', views.get_cards_by_category, name='category'),
    path('tags/<int:tag_id>/', views.get_cards_by_tag, name='get_cards_by_tag'),
    path('<int:card_id>/detail/', views.get_detail_card_by_id, name='detail_card_by_id'),
    path('add/', views.add_card, name='add_card'),
]