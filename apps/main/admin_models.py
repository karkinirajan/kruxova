# ******************************************
# IMPORTS python
# ******************************************

# ******************************************
# IMPORTS django
# ******************************************
from django.contrib import admin


class Admin_Model_Data(admin.ModelAdmin):
    list_display = (
        "id",
        "indicator",
        "datasource",
        "location",
        "value_type",
        "period",
        "value",
        "created_at",
        "updated_at",
    )

    list_filter = ("indicator", "datasource", "value_type", "period", "created_at", "updated_at")
