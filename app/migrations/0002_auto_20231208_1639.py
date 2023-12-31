# Generated by Django 2.2.28 on 2023-12-08 13:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-date'], 'verbose_name': 'Комментарии к статье блога', 'verbose_name_plural': 'Комментарии к статьям блога'},
        ),
        migrations.AlterField(
            model_name='blog',
            name='posted',
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2023, 12, 8, 16, 39, 42, 328050), verbose_name='Опубликовано'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2023, 12, 8, 16, 39, 42, 328050), verbose_name='Дата комментария'),
        ),
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2023, 12, 8, 16, 39, 42, 331019), verbose_name='Дата создания'),
        ),
    ]
