from datetime import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
import uuid

time = timezone
# Create your models here.

class User(models.Model):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        USER = "USER", "User"
    
    Uid = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    base_role = Role.ADMIN
    role = models.CharField(max_length=50, choices=Role.choices)
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(max_length=50)
    contacts = models.IntegerField(blank=False)
    password = models.CharField(max_length=15)


    REQUIRED_FIELDS = ["email", "contacts", "password", "re_password"]
    USERNAME_FIELD = "username"

    def __str__(self) -> str:
        return self.username

class Document(models.Model):
    document_id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    class Colors(models.TextChoices):
        COLORED = "Colored", "Colored"
        BLACK_AND_WHITE = "B&W", "Black_and_white"
    document_color = models.CharField(choices=Colors.choices, max_length=7)
    number_of_copies = models.IntegerField()
    pages_to_print = models.IntegerField()
    date = models.DateTimeField()
    amount = models.IntegerField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

class Print_log(models.Model):
    printlog_id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    status = models.CharField(max_length=20)
    time = models.DateTimeField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    document_id = models.ForeignKey(Document, on_delete=models.CASCADE)

class Notification(models.Model):
    notification_id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    message = models.CharField(max_length=30)
    time = models.DateTimeField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    printlog_id = models.ForeignKey(Print_log, on_delete=models.CASCADE)

class Payment_Receipt(models.Model):
    receipts_id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    amount_remaining = models.IntegerField()
    date = models.DateTimeField()
    document_id = models.ForeignKey(Document, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

class Print_Queue(models.Model):
    printqueue_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    printlog_id = models.ForeignKey(Print_log, on_delete=models.CASCADE)
    document_id = models.ForeignKey(Document, on_delete=models.CASCADE)
    


