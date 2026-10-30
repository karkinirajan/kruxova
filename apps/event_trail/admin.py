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
from apps.event_trail import models

# Register your models here.
admin.site.register(models.TrailRequest)
