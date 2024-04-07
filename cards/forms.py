from django import forms
from cards.models import Category, Card, Tag


class CardForm(forms.Form):
    question = forms.CharField(label='Вопрос', max_length=100, min_length=3,
                               error_messages={'required': 'Поле не может быть пустым',
                                               'min_length': 'Минимум 3 символа!'})
    answer = forms.CharField(label='Ответ', min_length=10, widget=forms.Textarea(attrs={'rows': 10, 'cols': 20}),
                             error_messages={'min_length': 'Минимум 10 символов'})
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категория', empty_label='Вне категории',
                                      required=True)


class CardModelForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Категория не выбрана",
                                      label="Категории")
    tags = forms.CharField(label="Теги", required=False, help_text="Перечислите теги чере запятую")

    class Meta:
        model = Card
        fields = ['question', 'answer', 'category', 'tags']
        widgets = {
            'question': forms.TextInput(attrs={'class': 'form-control'}),
            'answer': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'cols': 40})
        }
        labels = {
            'question': 'Вопрос',
            'answer': 'Ответ'
        }

    def clean_tags(self):
        tags_str = self.cleaned_data['tags']
        tag_list = [tag.strip() for tag in tags_str.split(',') if tag.strip()]
        return tag_list

    def save(self, *args, **kwargs):
        instance = super().save(commit=False)
        instance.save()

        self.instance.tags.clear()

        tag_names = self.cleaned_data['tags'].split(',')
        for tag_name in tag_names:
            tag_name = tag_name.strip()
            if tag_name:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                self.instance = tags.add(tag)

        return instance
