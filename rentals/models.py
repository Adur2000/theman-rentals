from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.conf import settings


HOUSE_CATEGORIES = [
    ('Bedsitter', 'Bedsitter'),
    ('1 Bedroom', '1 Bedroom'),
    ('2 Bedroom', '2 Bedroom'),
    ('Story Building', 'Story Building'),
]

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('CEO', 'CEO'),
        ('Manager', 'Manager'),
        ('Landlord', 'Landlord'),
        ('Rider', 'Rider'),
        ('Tenant', 'Tenant'),
    ]
    phone = models.CharField(max_length=15, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Tenant')

    def __str__(self):
        return self.username


class Landlord(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    phone = models.CharField(max_length=15)
    area = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username if self.user else 'NoUser'} - {self.area}"


class Rider(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    area = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.user.username if self.user else 'NoUser'} - {self.area} - {self.price}"


class House(models.Model):
    title = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='house_images/', blank=True, null=True)
    is_booked = models.BooleanField(default=False)
    landlord = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)


class HouseImage(models.Model):
    house = models.ForeignKey(House, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='house_images/')
    caption = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Image for {self.house.title}"


class Booking(models.Model):
    tenant = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    national_id = models.CharField(max_length=20)
    phone = models.CharField(max_length=15)
    occupation = models.CharField(max_length=100)
    move_in = models.DateField()
    notes = models.TextField(blank=True)
    location = models.CharField(max_length=100)
    distance_km = models.FloatField(null=True, blank=True)
    urgency_level = models.CharField(max_length=20, choices=[('normal', 'Normal'), ('urgent', 'Urgent')], default='normal')
    created_at = models.DateTimeField(auto_now_add=True)


class SMSLog(models.Model):  # ✅ renamed to camel-case for consistency
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.action} - {self.status}"