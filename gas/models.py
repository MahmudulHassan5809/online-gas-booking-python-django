from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
import random
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
        return self.name


def create_new_ref_number():
    return str(random.randint(1000000000, 9999999999))


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
        return self.name


class Booking(models.Model):
    REFFILING_SIZE = (
        ('14.2', '14.2 KG'),
        ('5', '5 KG'),
        ('3', '3 KG'),
    )

    BOOKING_STATUS = (
        ('1', 'Confirmed'),
        ('2', 'On The Way'),
        ('3', 'Delivered'),
    )

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_bookings')
    connection = models.ForeignKey(Connection, on_delete=models.CASCADE)
    reffeling_size = models.CharField(max_length=10, choices=REFFILING_SIZE)
    booking_number = models.CharField(
        max_length=10,
        blank=True,
        editable=False,
        unique=True,
        default=create_new_ref_number()
    )
    status = models.CharField(max_length=10, choices=BOOKING_STATUS)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    date = models.DateField()
