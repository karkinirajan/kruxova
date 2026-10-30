from django.db import models
from django.utils import timezone as django_util_timezone

# Create your models here.


class Interest(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=255)
    dashboard = models.CharField(max_length=255)
    created = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(blank=False, null=False, default=django_util_timezone.now)
    updated_at = models.DateTimeField(blank=False, null=False, default=django_util_timezone.now)

    def __str__(self):
        return ("{}/{}").format(self.email, self.dashboard)

    class Meta:
        managed = True
        # db_table = 'interest'
