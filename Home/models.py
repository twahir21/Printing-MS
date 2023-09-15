from datetime import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
import uuid

time = timezone
# Create your models here.

class User(models.Model):
    Uid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(max_length=50)
    contacts = models.IntegerField(blank=False)
    password = models.CharField(max_length=15)

    REQUIRED_FIELDS = ["email", "contacts", "password"]
    USERNAME_FIELD = "username"

    def __str__(self) -> str:
        return self.username

class Admin(models.Model):
    aid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    admin_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(max_length=50)
    contacts = models.IntegerField(blank=False)
    password = models.CharField(max_length=15)

    REQUIRED_FIELDS = ["email", "contacts", "password"]
    USERNAME_FIELD = "username"

    def __str__(self) -> str:
        return self.username

class Document(models.Model):
    document_id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    file = models.FileField()
    class Colors(models.TextChoices):
        COLORED = "Colored", "Colored"
        BLACK_AND_WHITE = "B&W", "Black_and_white"
    document_color = models.CharField(choices=Colors.choices, max_length=7)
    class Number_of_copies(models.TextChoices):
        ONE = "1", "1"
        TWO = "2", "2"
        THREE = "3", "3"
        FOUR = "4", "4"
        FIVE = "5", "5"
        SIX = "6", "6"
    number_of_copies = models.CharField(choices=Number_of_copies.choices, max_length=5)
    # pages_to_print = models.IntegerField()
    date = models.DateTimeField()
    name = models.CharField(max_length=30)
    # amount = models.IntegerField()
    # user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    user_id = models.CharField(max_length=100)

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
    


