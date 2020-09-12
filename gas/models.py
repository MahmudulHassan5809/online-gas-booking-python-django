from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
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


class Connection(models.Model):
    STATUS_CHOICES = (
        ('1', 'Approved'),
        ('2', 'On Hold'),
        ('3', 'Rejected'),
    )

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='user_connection')
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    mobile = models.CharField(max_length=20)
    gender = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    id_proof = models.ImageField(upload_to='connection')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    class Meta:
        verbose_name = 'Connection'
        verbose_name_plural = '2. New Connection'

    def get_absolute_url(self):
        return reverse('gas:view_connection', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name
