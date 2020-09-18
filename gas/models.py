from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
import random
from django.utils.crypto import get_random_string
# Create your models here.


User = get_user_model()


class Staff(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='staff')
    mobile = models.CharField(max_length=20)
    address = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Staff'
        verbose_name_plural = '1. Delivery Staff'

    def __str__(self):
        return self.user.username


def create_new_ref_number():
    return get_random_string(8)


class Connection(models.Model):
    STATUS_CHOICES = (
        ('1', 'Approved'),
        ('2', 'On Hold'),
        ('3', 'Rejected'),
    )

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='user_connection')
    connection_number = models.CharField(
        max_length=10,
        blank=True,
        editable=False,
        unique=True,
        default=create_new_ref_number()
    )
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    mobile = models.CharField(max_length=20)
    gender = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    id_proof = models.ImageField(upload_to='connection')
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='2')

    class Meta:
        verbose_name = 'Connection'
        verbose_name_plural = '2. New Connection'

    def get_absolute_url(self):
        return reverse('gas:view_connection', kwargs={'pk': self.pk})

    def __str__(self):
        return self.connection_number


class GasReffiling(models.Model):
    reffiling_size = models.CharField(max_length=50)
    price = models.FloatField()

    class Meta:
        verbose_name = 'GasReffiling'
        verbose_name_plural = '3.Gas Reffiling'

    def __str__(self):
        return self.reffiling_size


class Booking(models.Model):
    BOOKING_STATUS = (
        ('1', 'Confirmed'),
        ('2', 'On The Way'),
        ('3', 'Delivered'),
    )

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_bookings')
    connection = models.ForeignKey(Connection, on_delete=models.CASCADE)
    reffiling = models.ForeignKey(GasReffiling, on_delete=models.CASCADE)
    booking_number = models.CharField(
        max_length=10,
        blank=True,
        editable=False,
        unique=True,
        default=create_new_ref_number()
    )
    status = models.CharField(
        max_length=10, choices=BOOKING_STATUS, null=True, blank=True)
    staff = models.ForeignKey(
        Staff, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(auto_now_add=True, auto_now=False)

    class Meta:
        verbose_name = 'Booking'
        verbose_name_plural = '4.Booking'

    def __str__(self):
        return self.booking_number
