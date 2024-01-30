from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True, null=True, blank=True)
    emailVerified = models.DateTimeField(null=True, blank=True)
    image = models.CharField(max_length=255, null=True, blank=True)

    provider = models.CharField(max_length=255, null=True, blank=True)
    providerAccountId = models.CharField(max_length=255, null=True, blank=True)
