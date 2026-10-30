from django.db import models
from django.contrib.auth import get_user_model


class Group(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(blank=False, null=False)
    decription = models.TextField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return ("{}/{}").format(self.id, self.name)


class LocationHierarchyLevel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return ("{}/{}").format(self.id, self.name)

    class Meta:
        managed = True
        # db_table = 'location_hierarchy_level'


class Location(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(blank=False, null=False)
    parent = models.IntegerField(blank=True, null=True)
    level = models.ForeignKey("LocationHierarchyLevel", on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return ("ID:{},NAME:{},LEVEL:{},PARENT:{}").format(
            self.id, self.name, self.level, self.parent
        )

    class Meta:
        managed = True
        # db_table = 'location'


class ValueType(models.Model):
    id = models.AutoField(primary_key=True)
    value_type = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.value_type

    class Meta:
        managed = True
        # db_table = 'value_type'


class Factor(models.Model):
    id = models.AutoField(primary_key=True)
    multiplier_factor = models.IntegerField()
    display_factor = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.display_factor

    class Meta:
        managed = True
        # db_table = 'factor'


class Datasource(models.Model):
    id = models.AutoField(primary_key=True)
    datasource = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)
    description = models.TextField()
    year_available = models.CharField(max_length=255)
    period_available = models.CharField(max_length=255)
    methodology = models.TextField()
    subnational_data = models.CharField(max_length=255)
    classification = models.CharField(max_length=255)
    group = models.ManyToManyField(
        "Group",
        related_name="group_datasource",
        verbose_name="the groups associated with this datasource",
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.datasource

    class Meta:
        managed = True
        # db_table = 'datasource'


class DatasourceValuetype(models.Model):
    datasource = models.ForeignKey("Datasource", on_delete=models.DO_NOTHING)
    valuetype = models.ForeignKey("ValueType", on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return ("{}/{}").format(self.datasource, self.valuetype)

    class Meta:
        managed = True
        # db_table = 'datasource_valuetype'


class DatasourceLocation(models.Model):
    datasource = models.ForeignKey("Datasource", on_delete=models.DO_NOTHING)
    location = models.ForeignKey("Location", on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return ("{}/{}").format(self.datasource, self.location)

    class Meta:
        managed = True
        # db_table = 'datasource_location'


class Indicator(models.Model):
    id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=255)
    factor = models.ForeignKey("Factor", on_delete=models.DO_NOTHING)
    # valuetype = models.ForeignKey('ValueType', on_delete=models.DO_NOTHING)
    desirable_slope = models.CharField(max_length=255)
    indicator_type = models.CharField(max_length=255)
    program_area = models.CharField(max_length=255)
    national_target = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    national_source = models.CharField(max_length=255, blank=True, null=True)
    national_information = models.CharField(max_length=255, blank=True, null=True)
    sdg_target = models.CharField(max_length=255, blank=True, null=True)
    sdg_information = models.CharField(max_length=255, blank=True, null=True)
    first_related = models.IntegerField(blank=True, null=True)
    second_related = models.IntegerField(blank=True, null=True)
    third_related = models.IntegerField(blank=True, null=True)
    fourth_related = models.IntegerField(blank=True, null=True)
    datasources = models.ManyToManyField(Datasource, related_name="indicators")
    group = models.ManyToManyField(
        "Group",
        related_name="group_indicator",
        verbose_name="the groups associated with this datasource",
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return ("{}/{}").format(self.id, self.full_name)

    class Meta:
        managed = True
        # db_table = 'indicator'


class IndicatorValuetype(models.Model):
    indicator = models.ForeignKey("Indicator", on_delete=models.DO_NOTHING)
    valuetype = models.ForeignKey("ValueType", on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return "{}/{}".format(self.indicator, self.valuetype)

    class Meta:
        managed = True
        # db_table = 'indicator_valuetype'


class DatasourceSpecificIndicator(models.Model):
    id = models.AutoField(primary_key=True)
    datasource = models.ForeignKey("Datasource", on_delete=models.DO_NOTHING)
    indicator = models.ForeignKey("Indicator", on_delete=models.DO_NOTHING)
    datasource_indicator = models.CharField(max_length=255)
    measurement_numerator = models.TextField()
    measurement_denominator = models.TextField()
    frequency = models.CharField(max_length=255)
    methodology_estimation = models.TextField()
    indicator_definition = models.TextField()
    data_level = models.CharField(max_length=255)
    national = models.BooleanField(blank=True, null=True)
    zonal = models.BooleanField(blank=True, null=True)
    state = models.BooleanField(blank=True, null=True)
    senatorial = models.BooleanField(blank=True, null=True)
    lga = models.BooleanField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return "DATASOURCE:{},INDICATOR:{}".format(self.datasource, self.indicator)

    class Meta:
        managed = True
        # db_table = 'datasource_specific_indicator'


class Link(models.Model):
    id = models.AutoField(primary_key=True)
    datasource = models.ForeignKey("Datasource", on_delete=models.DO_NOTHING)
    period = models.CharField(max_length=255, blank=True, null=True)
    indicator = models.ForeignKey("Indicator", on_delete=models.DO_NOTHING, blank=True, null=True)
    link = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return "{}/{}".format(self.indicator, self.datasource)

    class Meta:
        managed = True
        # db_table = 'link'


class Data(models.Model):
    id = models.AutoField(primary_key=True)
    indicator = models.ForeignKey("Indicator", on_delete=models.DO_NOTHING)
    period = models.CharField(max_length=255)
    location = models.ForeignKey("Location", on_delete=models.DO_NOTHING)
    datasource = models.ForeignKey("Datasource", on_delete=models.DO_NOTHING)
    value_type = models.ForeignKey("ValueType", on_delete=models.DO_NOTHING)
    value = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return "ID-{}/CREATED-{}/UPDATED-{}".format(self.id, self.created_at, self.updated_at)

    class Meta:
        managed = True
        # db_table = 'data'

        unique_together = [
            "indicator",
            "period",
            "location",
            "datasource",
            "value_type",
        ]

    def save(self, *args, **kwargs):
        self.indicator.datasources.add(self.datasource)
        self.indicator.save()
        return super().save(*args, **kwargs)


GENDER_CHOICES = [["MALE", "MALE"], ["FEMALE", "FEMALE"]]


class DisaggregatedData(models.Model):
    """
    This is the model for storing disaggregated data
    such as demographics data
    """

    id = models.AutoField(primary_key=True)
    indicator = models.ForeignKey("Indicator", on_delete=models.DO_NOTHING)
    period = models.CharField(max_length=255)
    location = models.ForeignKey("Location", on_delete=models.DO_NOTHING)
    datasource = models.ForeignKey("Datasource", on_delete=models.DO_NOTHING)
    value_type = models.ForeignKey("ValueType", on_delete=models.DO_NOTHING)
    value = models.CharField(max_length=255, blank=True, null=True)
    age = models.CharField(max_length=20, null=True, blank=True)
    gender = models.CharField(max_length=7, choices=GENDER_CHOICES, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)


class Subscriber(models.Model):
    """
    This is an email newsletter subscriber, this is the model to
    store the subscribers details
    """

    name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return f"{self.name}-{self.email}"

    class Meta:
        managed = True
        unique_together = ["name", "email"]


class Dashboard(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    indicators = models.ManyToManyField(Indicator, related_name="dashboards")
    datasources = models.ManyToManyField(Datasource, related_name="dashboards")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s {self.name} dashboard"
