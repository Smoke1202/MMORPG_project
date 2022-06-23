from django.db import models

from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


class Category(models.Model):
    TYPE = (
        ('tank', 'Танки'),
        ('heal', 'Хилы'),
        ('dd', 'ДД'),
        ('buyers', 'Торговцы'),
        ('gildemaster', 'Гилдмастеры'),
        ('quest', 'Квестгиверы'),
        ('smith', 'Кузнецы'),
        ('tanner', 'Кожевники'),
        ('potion', 'Зельевары'),
        ('spellmaster', 'Мастера заклинаний'),
    )
    category_name = models.CharField(max_length=255, choices=TYPE, unique=True,)
    subscribers = models.ManyToManyField(User, null=True, blank=True, related_name='subscriber')

    def __str__(self):
        return f'{self.category_name}'


class Article(models.Model):

    author = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    text = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    upload = models.FileField(upload_to='uploads/', blank=True)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    def get_absolute_url(self): # добавим абсолютный путь чтобы после создания нас перебрасывало на страницу с новостью
        return reverse('article-detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    # connecting Comment model with Bulletin model
    article = models.ForeignKey(Article, related_name="comments", on_delete=models.CASCADE)
    username = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.article.title, self.username)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('comment_create', kwargs={'pk': self.pk})
