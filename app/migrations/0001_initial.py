# Generated by Django 2.2.28 on 2023-12-08 13:06

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique_for_date='posted', verbose_name='Заголовок')),
                ('descriprion', models.TextField(verbose_name='Краткое содержание')),
                ('content', models.TextField(verbose_name='Полное содержание')),
                ('posted', models.DateTimeField(db_index=True, default=datetime.datetime(2023, 12, 8, 16, 6, 52, 8303), verbose_name='Опубликовано')),
                ('image', models.FileField(default='temp', upload_to='', verbose_name='Путь к картинке')),
            ],
            options={
                'verbose_name': 'Статья блога',
                'verbose_name_plural': 'статьи блога',
                'db_table': 'Posts',
                'ordering': ['-posted'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=100, verbose_name='Наименование')),
                ('content', models.TextField(blank=True, verbose_name='Описание')),
                ('price', models.FloatField(verbose_name='Цена')),
                ('is_course', models.BooleanField(default=False, verbose_name='Является курсом')),
                ('lessons_count', models.IntegerField(default=-1, verbose_name='Количество занятий')),
                ('full_course_price', models.FloatField(default=-1, verbose_name='Цена за весь курс со скидкой')),
                ('stock', models.PositiveIntegerField(verbose_name='Количество на складе')),
                ('image', models.FileField(default='temp', upload_to='', verbose_name='Путь к картинке')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
                'db_table': 'Products',
                'ordering': ['-price'],
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.TextField(verbose_name='Данные заказа')),
                ('state', models.CharField(choices=[('new', 'Новый'), ('confirmed', 'Подтвержденный'), ('canceled', 'Отмененный'), ('delivered', 'Доставленный'), ('returned', 'Возвратный'), ('completed', 'Завершенный')], default='new', max_length=20, verbose_name='Статус заказа')),
                ('date', models.DateTimeField(db_index=True, default=datetime.datetime(2023, 12, 8, 16, 6, 52, 11354), verbose_name='Дата создания')),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Покупатель')),
                ('products', models.ManyToManyField(to='app.Product', verbose_name='Товары')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
                'db_table': 'Orders',
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Текст комментария')),
                ('date', models.DateTimeField(db_index=True, default=datetime.datetime(2023, 12, 8, 16, 6, 52, 8303), verbose_name='Дата комментария')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор комментария')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Blog', verbose_name='Статья комментария')),
            ],
            options={
                'verbose_name': 'Комментарии к статьям блога',
                'db_table': 'Comment',
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Владелец')),
                ('products', models.ManyToManyField(to='app.Product', verbose_name='Товары')),
            ],
            options={
                'verbose_name': 'Корзина',
                'verbose_name_plural': 'Корзины',
                'db_table': 'Cart',
            },
        ),
    ]
