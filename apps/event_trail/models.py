# *****************************************
# IMPORTs django
# *****************************************
from django.contrib.auth import models as django_auth_models
from django.db import models


class TrailRequest(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(django_auth_models.User, on_delete=models.DO_NOTHING)
    method = models.CharField(max_length=12, blank=True, null=True)
    request = models.TextField(blank=True, null=True)
    response = models.TextField(blank=True, null=True)
    logged_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return ("{}/{}/{}").format(self.id, self.user, self.logged_on)
