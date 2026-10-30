# *****************************************
# IMPORTs python
# *****************************************

# *****************************************
# IMPORTs django
# *****************************************
from django.contrib import admin
from rest_framework.authtoken.admin import TokenAdmin

# *****************************************
# IMPORTs shared
# *****************************************

# *****************************************
# IMPORTs app
# *****************************************
from apps.main import models
from apps.main import admin_models

# Register your models here.
admin.site.register(models.Group)

admin.site.register(models.Location)

admin.site.register(models.LocationHierarchyLevel)

admin.site.register(models.ValueType)

admin.site.register(models.Factor)

admin.site.register(models.Datasource)

admin.site.register(models.DatasourceValuetype)

admin.site.register(models.DatasourceLocation)

admin.site.register(models.DatasourceSpecificIndicator)

admin.site.register(models.Indicator)

admin.site.register(models.IndicatorValuetype)

admin.site.register(models.Link)

admin.site.register(models.Data, admin_models.Admin_Model_Data)

TokenAdmin.raw_id_fields = ["user"]
