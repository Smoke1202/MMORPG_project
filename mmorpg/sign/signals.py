from allauth.account.signals import email_confirmed
from django.core.mail import mail_managers, send_mail
from django.db.models.signals import post_save
from django.contrib.auth.models import User # User is sender
from django.dispatch import receiver
from .models import Profile


@receiver(post_save, sender=User) # when a user was saved, it creates a signal
# post_save --> this signal is received by @receiver
def create_profile(sender, instance, created, **kwargs): # these arguments are passed by post_save
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User) # when a user was saved, it creates a signal
# post_save --> this signal is received by @receiver
def save_profile(sender, instance, **kwargs): # these arguments are passed by post_save
    instance.profile.save()


@receiver(email_confirmed)
def user_signed_up(request, email_address, **kwargs):
    # отправляется письмо пользователю, чья почта была подтверждена
    send_mail(
        subject=f'Dear {email_address.user} Welcome to my News Portal!',
        message=f'Приветствую Вас на моём новостном портале. Здесь самые последние новости из разных категорий',
        from_email='Christopherga@yandex.ru',
        recipient_list=[email_address.user.email]
    )