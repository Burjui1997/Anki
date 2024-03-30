from django.db import models

# Create your models here.
class Card(models.Model):
     card_id = models.AutoField(primary_key=True, db_column="CardID")
     question = models.TextField(db_column="Question")
     answer = models.TextField(db_column="Answer")
     category_id = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, db_column="CategoryID")
     upload_date = models.DateTimeField(auto_now_add=True, db_column="UploadDate")
     views = models.IntegerField(default=0, db_column="Views")
     favorites = models.IntegerField(default=0, db_column="Favorites")
     tags = models.ManyToManyField('Tag', related_name='cards', through="CardTags")

     # Расширение нашего класса
     class Meta:
         db_table = 'Cards'
         verbose_name = 'Карточка'
         verbose_name_plural = 'Карточки'

     def __str__(self):
         return self.question

     def get_absolute_url(self):
         return reverse('detail_card_by_id', kwargs={'card_id': self.card_id})

# Тестируем связь многие ко многим (ManyToManyField), создаем для примера класс Tag

class Category(models.Model):
    category_id = models.AutoField(primary_key=True, db_column="CategoryID")
    name = models.CharField(max_length=100, unique=True, db_column="Name")

    class Meta:
        db_table = "Categories"
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

class User(models.Model):
    user_id = models.AutoField(primary_key=True, db_column="UserID")
    user_name = models.TextField(max_length=100, db_column="UserName")

    class Meta:
        db_table = "Users"
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.user_name

class Tag(models.Model):
    tag_id = models.AutoField(primary_key=True, db_column="TagID")
    name = models.CharField(max_length=50, unique=True, db_column="Name")

    class Meta:
        db_table = "Tags"
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name
"""
Добавляем теги
tag1 = Tag.objects.create(name="Python")
tag2 = Tag.objects.create(name="Django")
tag3 = Tag.objects.create(name="Flask")
Сохраняем теги
Создаем карточки с тегами
card = Card.objects.create(question="Как создать карточку?", answer="Использовать метод Create()")
card.tags.add(tag1, tag2)
Добываем последнюю карточку
last_card = Card.objects.last()
Получаем все теги
tag_all = card.tags.all()
"""

class CardTags(models.Model):
    id = models.AutoField(primary_key=True, db_column='ID')
    card = models.ForeignKey('Card', on_delete=models.CASCADE, db_column='CardID')
    tag = models.ForeignKey('Tag', on_delete=models.CASCADE, db_column='TagID')

    class Meta:
        db_table = 'CardTags'
        verbose_name = 'Связь карточка-тег'
        verbose_name_plural = 'Связи карточка-тег'

    def __str__(self):
        return f'{self.card} - {self.tag}'




