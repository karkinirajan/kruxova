from django.db import models

CACHE_NAME_ALL_DATA = "all_data"
CACHE_NAME_MASTER_SHEET = "master_sheet"
CACHE_NAME_LGA_DATA = "lga_data"
CACHE_NAME_ESTIMATES_DATA = "estimates_data"
# register here names of data-cache files
CACHE_NAMES = {
    CACHE_NAME_ALL_DATA: CACHE_NAME_ALL_DATA,
    CACHE_NAME_MASTER_SHEET: CACHE_NAME_MASTER_SHEET,
    CACHE_NAME_ESTIMATES_DATA: CACHE_NAME_ESTIMATES_DATA,
    CACHE_NAME_LGA_DATA: CACHE_NAME_LGA_DATA,
}

CHOICES_STATUS_EMPTY = "EMPTY"
CHOICES_STATUS_INPROGRESS = "IN-PROGRESS"
CHOICES_STATUS_COMPLETED = "COMPLETED"
CHOICES_STATUS_FAILED = "FAILED"
CHOICES_STATUS = [
    (CHOICES_STATUS_EMPTY, CHOICES_STATUS_EMPTY),
    (CHOICES_STATUS_INPROGRESS, CHOICES_STATUS_INPROGRESS),
    (CHOICES_STATUS_COMPLETED, CHOICES_STATUS_COMPLETED),
    (CHOICES_STATUS_FAILED, CHOICES_STATUS_FAILED),
]

CHOICES_CACHE_TYPE_FILE = "FILE"
CHOICES_CACHE_TYPE_MEMORY = "MEMORY"
CHOICES_CACHE_TYPE = [
    (CHOICES_CACHE_TYPE_FILE, CHOICES_CACHE_TYPE_FILE),
    (CHOICES_CACHE_TYPE_MEMORY, CHOICES_CACHE_TYPE_MEMORY),
]


# Create your models here.
class DataCacheStatus(models.Model):
    cache_name = models.TextField(primary_key=True, blank=False, null=False)
    cache_type = models.TextField(blank=False, null=False, choices=CHOICES_CACHE_TYPE)
    status = models.TextField(blank=False, null=False, choices=CHOICES_STATUS)
    error = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return "{}/{}".format(self.cache_type, self.cache_name)

    class Meta:
        unique_together = ["cache_name", "cache_type"]
