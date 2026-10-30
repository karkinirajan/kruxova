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
from apps.data_caches import models

# Register your models here.
admin.site.register(models.DataCacheStatus)
