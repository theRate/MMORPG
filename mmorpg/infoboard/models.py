from django.contrib.auth.models import User
from django.db import models
from ckeditor.fields import RichTextField


# Create your models here.
class Post(models.Model):
    TANK = 'TK'
    HEALER = 'HL'
    DAMAGE_DEALER = 'DD'
    TRADER = 'TD'
    GUILD_MASTER = 'GM'
    QUEST_GIVER = 'QG'
    BLACKSMITH = 'BS'
    TANNER = 'TN'
    POTIONS_MASTER = 'PM'
    SPELL_MASTER = 'SM'
    CATEGORIES = [
        (TANK, 'Танки'),
        (HEALER, 'Хилы'),
        (DAMAGE_DEALER, 'ДД'),
        (TRADER, 'Торговцы'),
        (GUILD_MASTER, 'Гилдмастеры'),
        (QUEST_GIVER, 'Квестгиверы'),
        (BLACKSMITH, 'Кузнецы'),
        (TANNER, 'Кожевники'),
        (POTIONS_MASTER, 'Зельевары'),
        (SPELL_MASTER, 'Мастера заклинаний'),
    ]

    title = models.CharField(max_length=128, verbose_name='Заголовок')
    content = RichTextField(verbose_name='Содержание')
    category = models.CharField(max_length=2, choices=CATEGORIES, default=TANK, verbose_name='Категория')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_c = models.DateTimeField(auto_now_add=True)
    date_u = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/{self.id}'


class Response(models.Model):
    text = models.TextField(verbose_name='Отклик')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Объявление')
    date_c = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.post} !--> {self.author}: {self.text}'
