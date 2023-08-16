from django.conf import settings
from django.core.mail import send_mail

from .models import Response



def notify_new_response(pk):
    response = Response.objects.get(id=pk)
    send_mail(
        subject=f'MMORPG - new response to your post!',
        message=f'Привет, {response.post.author}!\n'
                f'На ваше объявление "{response.post.title}" есть новый отклик.\n'
                f'{response.author}: "{response.text}", ',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[response.post.author.email, ],
    )


def notify_approved_response(pk):
    response = Response.objects.get(id=pk)
    send_mail(
        subject=f'MMORPG - your response is approved!',
        message=f'Привет, {response.author}!\n'
                f'Ваш отклик на объявление "{response.post.title}" принят.\n'
                f'Посмотреть объявление целиком можно по ссылке:\n'
                f'http://127.0.0.1:8000/{response.post.id}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[response.author.email, ],
    )
