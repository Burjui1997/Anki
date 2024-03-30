from django.contrib import admin
from .models import Card, Tag, Category, CardTags
# Register your models here.

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('get_question', 'upload_date', 'category_name', 'tags_list')
    list_display_links = ('get_question', 'category_name')
    list_filter = ('category_id',)
    search_fields = ('question', 'category_id__name', 'answer' ,'tags__name',)
    ordering = ('-upload_date', 'question')
    def category_name(self, obj):
        return obj.category_id.name
    category_name.short_description = 'Категория'

    def tags_list(self, obj):
        return " | ".join([tag.name for tag in obj.tags.all()])
    tags_list.short_description = 'Теги'

    def get_question(self, obj):
        row_question = obj.question
        return row_question.replace('##', '').replace('`', '').replace('**', '').replace('*', '')
    get_question.short_description = 'Вопрос'

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

# @admin.register(CardTags)
# class CardTagsAdmin(admin.ModelAdmin):
#     list_display = ('card', 'tag')