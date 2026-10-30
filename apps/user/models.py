from django.db import models
from django.utils import timezone as django_util_timezone


# Create your models here.
class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    profession = models.CharField(max_length=255)
    organization = models.CharField(max_length=255)
    email = models.CharField(unique=True, max_length=255)
    created_at = models.DateTimeField(blank=False, null=False, default=django_util_timezone.now)
    updated_at = models.DateTimeField(blank=False, null=False, default=django_util_timezone.now)

    def __str__(self):
        return ("{}/{}").format(self.id, self.email)

    class Meta:
        managed = True


class Contact(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(null=False, blank=False)
    email = models.TextField(null=False, blank=False, unique=False)
    profession = models.TextField(null=True, blank=True)
    organization = models.TextField(null=True, blank=True)
    category = models.TextField(null=True, blank=True)
    feedback = models.TextField(null=True, blank=True)
    newsletter = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return ("{}/{}").format(self.id, self.email)
