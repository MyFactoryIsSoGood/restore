from django.db import models


class Gadget(models.Model):
    CATEGORYS = [('phones', 'Смартфоны'), ('desktops', 'Компьтеры'), ('laptops', 'Ноутбуки')]
    name = models.CharField(max_length=100, verbose_name='Устройство')
    photo = models.ImageField(verbose_name='Фото')
    price = models.FloatField(verbose_name='Цена')
    category = models.CharField(max_length=30, choices=CATEGORYS)

    def __str__(self):
        return self.name


class Comment(models.Model):
    class Rating(models.IntegerChoices):
        AWFUL = 1
        BAD = 2
        COMMON = 3
        GOOD = 4
        EXCELLENT = 5

    text = models.TextField(verbose_name='Отзыв')
    rating = models.IntegerField(choices=Rating.choices)
    author_name = models.CharField(max_length=20, verbose_name='Автор')
    date_published = models.DateField(verbose_name='Дата публикации', auto_now_add=True)
    to_item = models.ForeignKey(Gadget, on_delete=models.CASCADE, verbose_name='Товар')
