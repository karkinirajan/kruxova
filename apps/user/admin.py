# *****************************************
# IMPORTs python
# *****************************************

# *****************************************
# IMPORTs django
# *****************************************
from django.contrib import admin

# *****************************************
# IMPORTs shared
# *****************************************

# *****************************************
# IMPORTs app
# *****************************************
from apps.user import models

# Register your models here.
admin.site.register(models.User)

admin.site.register(models.Contact)
