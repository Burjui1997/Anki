# Generated by Django 4.2 on 2024-03-31 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='check_status',
            field=models.BooleanField(choices=[(False, 'Не проверено'), (True, 'Проверено')], db_column='CheckStatus', default=0),
        ),
        migrations.AlterField(
            model_name='card',
            name='upload_date',
            field=models.DateTimeField(auto_now_add=True, db_column='UploadDate', verbose_name='Дата загрузки'),
        ),
    ]