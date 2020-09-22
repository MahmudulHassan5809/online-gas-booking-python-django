from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from django.dispatch import receiver
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save

# Create your models here.


class User(AbstractUser):
    email = models.EmailField(unique=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = '1. User'


class Profile(models.Model):
    user = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE, related_name='user_profile')
    phone_number = models.CharField(max_length=50)
    address = models.CharField(max_length=50, blank=True, null=True)

    active = models.BooleanField(default=True)
    email_confirmed = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = '2. Profile'

    def __str__(self):
        return self.user.username


class PaymentCreditCard(models.Model):
    owner = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name='user_payment_credit_card')
    card_holder = models.CharField(max_length=250)
    card_number = models.CharField(max_length=255)
    expiration = models.DateTimeField()
    security_code = models.CharField(max_length=4, validators=[
                                     RegexValidator(r'^\d{1,10}$')])
    postal_code = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'PaymentCreditCard'
        verbose_name_plural = '3. PaymentCreditCard'

    def get_absolute_url(self):
        return reverse('accounts:payment_details')

    def __str__(self):
        return self.card_holder


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    try:
        if created:
            Profile.objects.create(user=instance)
        else:
            instance.user_profile.save()
    except Exception as e:
        pass
