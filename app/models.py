"""
Definition of models.
"""

from django.db import models
from django.contrib import admin
from datetime import datetime
from django.urls import reverse
from django.contrib.auth.models import User


class Blog(models.Model):

    title = models.CharField(max_length = 100, unique_for_date = "posted", verbose_name = "Заголовок")

    descriprion = models.TextField(verbose_name = "Краткое содержание")

    content = models.TextField(verbose_name = "Полное содержание")

    posted = models.DateTimeField(default = datetime.now(), db_index = True, verbose_name = "Опубликовано")

    image = models.FileField(default = 'temp', verbose_name = "Путь к картинке")

    def get_absolute_url(self):
        return reverse("blogpost", args = [str(self.id)])

    def __str__(self):
        return self.title

    class Meta:
        db_table = "Posts"

        ordering = ["-posted"]

        verbose_name = "Статья блога"

        verbose_name_plural = "статьи блога"

admin.site.register(Blog)


class Comment(models.Model):
    text = models.TextField(verbose_name = "Текст комментария")

    date = models.DateTimeField(default = datetime.now(), db_index = True, verbose_name= "Дата комментария")

    author = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name = "Автор комментария")

    post = models.ForeignKey(Blog, on_delete = models.CASCADE, verbose_name = "Статья комментария")

    def __str__(self):
        return 'Комментарий %d %s к %s ' % (self.id, self.author, self.post)

    class Meta:
        db_table = "Comment"

        ordering = ["-date"]

        verbose_name = "Комментарии к статье блога"

        verbose_name_plural = "Комментарии к статьям блога"

admin.site.register(Comment)

class Course(models.Model):
    title = models.CharField(max_length = 100, db_index = True, verbose_name = "Наименование")

    content = models.TextField(blank = True, verbose_name = "Описание")

    price = models.FloatField(verbose_name = "Цена")

    lessons_count = models.IntegerField(default = -1, verbose_name = "Количество занятий")

    full_course_price = models.FloatField(default = -1, verbose_name = "Цена за весь курс со скидкой")

    start_date = models.TextField(blank = True, verbose_name = "Дата начала курса")
    fdate_date = models.TextField(blank = True, verbose_name = "Дата окончания курса")

    def __str__(self):
        return "%s %s %s" % (self.id, self.title, self.price)

    class Meta:
        db_table = "Courses"

        ordering = ["title"]

        verbose_name = "Курс"

        verbose_name_plural = "Курсы"

admin.site.register(Course)

class Enrollment (models.Model):
    owner = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name = "Владелец")

    course = models.ForeignKey(Course, on_delete = models.CASCADE, verbose_name = "Курс")

    state_choices = (
        ("new", "Новый"),
        ("enrolled", "Записаный"),
        ("canceled", "Отмененный"),
        ("completed", "Завершенный"),
    )

    state = models.CharField(max_length = 20, choices = state_choices, default = "new", verbose_name = "Статус записи")

    phone = models.CharField(max_length = 20, verbose_name = "Телефон")

    def __str__(self):
        return "%s %s" % (self.id, self.owner)

    class Meta:
        db_table = "Enrollment"

        verbose_name = "Запись на курс"

        verbose_name_plural = "Записи на курсы"

admin.site.register(Enrollment)

class Category (models.Model):
    title = models.CharField(max_length = 100, db_index = True, verbose_name = "Наименование")

    def __str__(self):
        return self.title

    class Meta:
        db_table = "Categories"

        verbose_name = "Категория"

        verbose_name_plural = "Категории"

admin.site.register(Category)

class Product(models.Model):
    title = models.CharField(max_length = 100, db_index = True, verbose_name = "Наименование")

    content = models.TextField(blank = True, verbose_name = "Описание")

    category = models.ForeignKey(Category, on_delete = models.CASCADE, null=True, verbose_name = "Категория")

    price = models.FloatField(verbose_name = "Цена")

    stock = models.PositiveIntegerField(verbose_name = "Количество на складе")

    image = models.FileField(default = 'temp', verbose_name = "Путь к картинке")

    def __str__(self):
        return "%s %s %s" % (self.id, self.title, self.price)

    class Meta:
        db_table = "Products"

        ordering = ["-price"]

        verbose_name = "Товар"

        verbose_name_plural = "Товары"

admin.site.register(Product)

class Cart(models.Model):
    owner = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name = "Владелец")

    products = models.ManyToManyField(Product, verbose_name = "Товары")

    data = models.TextField(default="{}", verbose_name = "Данные корзины")

    def __str__(self):
        return "%s %s" % (self.id, self.owner)

    class Meta:
        db_table = "Cart"

        verbose_name = "Корзина"

        verbose_name_plural = "Корзины"

admin.site.register(Cart)

class Order(models.Model):
    products = models.ManyToManyField(Product, verbose_name = "Товары")

    data = models.TextField(verbose_name = "Данные заказа")

    buyer = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name = "Покупатель")

    state_choices = (
        ("new", "Новый"),
        ("confirmed", "Подтвержденный"),
        ("canceled", "Отмененный"),
        ("delivered", "Доставленный"),
        ("returned", "Возвратный"),
        ("completed", "Завершенный"),
    )

    state = models.CharField(max_length = 20, choices = state_choices, default = "new", verbose_name = "Статус заказа")

    date = models.DateTimeField(default = datetime.now(), db_index = True, verbose_name = "Дата создания")

    def __str__(self):
        return "%s %s %s" % (self.id, self.data, self.buyer)

    class Meta:
        db_table = "Orders"

        ordering = ["-date"]

        verbose_name = "Заказ"

        verbose_name_plural = "Заказы"

admin.site.register(Order)


# Create your models here.
