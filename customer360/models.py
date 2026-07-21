from django.db import models


class Communication(models.Model):

    CHANNEL_CHOICES = [
        ('Email', 'Email'),
        ('Phone', 'Phone'),
        ('SMS', 'SMS'),
        ('WhatsApp', 'WhatsApp'),
        ('Chat', 'Chat'),
    ]

    DIRECTION_CHOICES = [
        ('Inbound', 'Inbound'),
        ('Outbound', 'Outbound'),
    ]

    customer_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    channel = models.CharField(
        max_length=20,
        choices=CHANNEL_CHOICES
    )

    direction = models.CharField(
        max_length=20,
        choices=DIRECTION_CHOICES
    )

    summary = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer_name