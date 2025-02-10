from djongo import models # type: ignore
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    _id = models.ObjectIdField()