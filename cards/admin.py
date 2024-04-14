from django.contrib import admin
from .models import Card, Tag, Category, CardTags
# Register your models here.

class CheckStatusFilter(admin.SimpleListFilter):
    title = 'Статус проверки'
    parameter_name = 'check_status'

    def lookups(self, request, model_admin):
        return (
            ('UNCHECKED', 'Не проверено'),
            ('CHECKED', 'Проверено')
        )
    def queryset(self, request, queryset):
        if self.value() == 'UNCHECKED':
            return queryset.filter(check_status=0)
        if self.value() == 'CHECKED':
            return queryset.filter(check_status=1)


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('get_question', 'upload_date', 'check_status', 'category_name', 'tags_list', 'brief_info',)
    list_display_links = ('get_question', 'category_name')
    list_editable = ('check_status',)
    list_filter = ('category_id', CheckStatusFilter,)
    search_fields = ('question', 'category_id__name', 'answer' ,'tags__name',)
    ordering = ('-upload_date', 'question')
    list_per_page = 20
    actions = ['make_checked', 'make_unchecked']
    fields = ('question', 'answer' 'category_id',)

    @admin.display(description='Категория', ordering='cattegory_id__name')
    def category_name(self, obj):
        return obj.category_id
    # category_name.short_description = 'Категория'

    @admin.display(description='Теги', ordering='tags__name')
    def tags_list(self, obj):
        return " | ".join([tag.name for tag in obj.tags.all()])
    # tags_list.short_description = 'Теги'

    @admin.display(description='Краткое описание', ordering='answer')
    def brief_info(self, card):
        length = len(card.answer)
        has_code = 'Да' if '``' in card.answer else 'Нет'
        return f'Длина ответа: {length}, Код: {has_code}'

    def get_question(self, obj):
        row_question = obj.question
        return row_question.replace('##', '').replace('`', '').replace('**', '').replace('*', '')
    get_question.short_description = 'Вопрос'

    @admin.action(description='Отметить выбранные карточки как проверенные')
    def make_checked(modeladmin, request, queryset):
        queryset.update(check_status=True)

    @admin.action(description='Отметить выбранные карточки как непроверенные')
    def make_unchecked(modeladmin, request, queryset):
        queryset.update(check_status=False)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(CardTags)
class CardTagsAdmin(admin.ModelAdmin):
    list_display = ('card', 'tag')