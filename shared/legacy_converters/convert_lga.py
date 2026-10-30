# ********************
# imports python
# ********************
# ********************
# imports django
# ********************
# ********************
# imports shared
# ********************
from shared.utils import utils_logger
from shared.legacy_converters import converter_utils

# ********************
# imports app
# ********************
from apps.main import models as main_models

# *************************************************************************
# API ROUTE
# *************************************************************************

PERIOD = {"start": 2000, "end": 2019}

response_model = [
    {"name": "Period", "indicator": "", "datasource": ""},  # 0
    {"name": "State", "indicator": "", "datasource": ""},  # 1
    {"name": "LGA & Senatorial District", "indicator": "", "datasource": ""},  # 2
    {
        "name": "ANC Coverage (4 visits) -> MICS",
        "indicator": "ANC Coverage (4 visits)",
        "datasource": "MICS",
    },  # 3
    {
        "name": "ANC Coverage (4 visits) -> NHMIS",
        "indicator": "ANC Coverage (4 visits)",
        "datasource": "NHMIS",
    },  # 4
    {
        "name": "ANC Coverage (at least 1 visit) -> KDGHS",
        "indicator": "ANC Coverage (at least 1 visit)",
        "datasource": "KDGHS",
    },  # 5
    {
        "name": "ANC Coverage (at least 1 visit) -> MICS",
        "indicator": "ANC Coverage (at least 1 visit)",
        "datasource": "MICS",
    },  # 6
    {
        "name": "ANC Coverage (at least 1 visit) -> NHMIS",
        "indicator": "ANC Coverage (at least 1 visit)",
        "datasource": "NHMIS",
    },  # 7
    {
        "name": "Adolescent birth rate -> MICS",
        "indicator": "Adolescent birth rate",
        "datasource": "MICS",
    },  # 8
    {
        "name": "Contraceptive prevalence rate -> MICS",
        "indicator": "Contraceptive prevalence rate",
        "datasource": "MICS",
    },  # 9
    {
        "name": "Contraceptive prevalence rate -> NHMIS",
        "indicator": "Contraceptive prevalence rate",
        "datasource": "NHMIS",
    },  # 10
    {
        "name": "DPT 3/Penta 3 coverage rate -> IHME",
        "indicator": "DPT 3/Penta 3 coverage rate",
        "datasource": "IHME",
    },  # 11
    {
        "name": "DPT 3/Penta 3 coverage rate -> KDGHS",
        "indicator": "DPT 3/Penta 3 coverage rate",
        "datasource": "KDGHS",
    },  # 12
    {
        "name": "DPT 3/Penta 3 coverage rate -> MICS",
        "indicator": "DPT 3/Penta 3 coverage rate",
        "datasource": "MICS",
    },  # 13
    {
        "name": "DPT 3/Penta 3 coverage rate -> NHMIS",
        "indicator": "DPT 3/Penta 3 coverage rate",
        "datasource": "NHMIS",
    },  # 14
    {
        "name": "IPV coverage rate -> NHMIS",
        "indicator": "IPV coverage rate",
        "datasource": "NHMIS",
    },  # 15
    {
        "name": "Infant Mortality rate -> MICS",
        "indicator": "Infant Mortality rate",
        "datasource": "MICS",
    },  # 16
    {
        "name": "Infant Mortality rate -> NHMIS",
        "indicator": "Infant Mortality rate",
        "datasource": "NHMIS",
    },  # 17
    {
        "name": "Maternal Mortality Ratio -> NHMIS",
        "indicator": "Maternal Mortality Ratio",
        "datasource": "NHMIS",
    },  # 18
    {
        "name": "Measles Immunization Coverage -> KDGHS",
        "indicator": "Measles Immunization Coverage",
        "datasource": "KDGHS",
    },  # 19
    {
        "name": "Measles Immunization Coverage -> MICS",
        "indicator": "Measles Immunization Coverage",
        "datasource": "MICS",
    },  # 20
    {
        "name": "Measles Immunization Coverage -> NHMIS",
        "indicator": "Measles Immunization Coverage",
        "datasource": "NHMIS",
    },  # 21
    {
        "name": "Measles Immunization Coverage -> PCCS",
        "indicator": "Measles Immunization Coverage",
        "datasource": "PCCS",
    },  # 22
    {
        "name": "Neonatal mortality rate (per 1000 live births) -> MICS",
        "indicator": "Neonatal mortality rate (per 1000 live births)",
        "datasource": "MICS",
    },  # 23
    {
        "name": "Neonatal mortality rate (per 1000 live births) -> NHMIS",
        "indicator": "Neonatal mortality rate (per 1000 live births)",
        "datasource": "NHMIS",
    },  # 24
    {
        "name": "Percentage of children fully immunized against childhood diseases by age 1 -> MICS",
        "indicator": "Percentage of children fully immunized against childhood diseases by age 1",
        "datasource": "MICS",
    },  # 25
    {
        "name": "Percentage of children fully immunized against childhood diseases by age 1 -> NHMIS",
        "indicator": "Percentage of children fully immunized against childhood diseases by age 1",
        "datasource": "NHMIS",
    },  # 26
    {
        "name": "Percentage of children under 5 with fever who received ACT -> MICS",
        "indicator": "Percentage of children under 5 with fever who received ACT",
        "datasource": "MICS",
    },  # 27
    {
        "name": "Percentage of children under 6 months who were exclusively breastfed -> IHME",
        "indicator": "Percentage of children under 6 months who were exclusively breastfed",
        "datasource": "IHME",
    },  # 28
    {
        "name": "Percentage of children under 6 months who were exclusively breastfed -> MICS",
        "indicator": "Percentage of children under 6 months who were exclusively breastfed",
        "datasource": "MICS",
    },  # 29
    {
        "name": "Percentage of children with diarrhoea who received treatment -> KDGHS",
        "indicator": "Percentage of children with diarrhoea who received treatment",
        "datasource": "KDGHS",
    },  # 30
    {
        "name": "Percentage of children with diarrhoea who received treatment -> MICS",
        "indicator": "Percentage of children with diarrhoea who received treatment",
        "datasource": "MICS",
    },  # 31
    {
        "name": "Percentage of people age 15-49 years who have been tested for HIV and know their results -> MICS",
        "indicator": "Percentage of people age 15-49 years who have been tested for HIV and know their results",
        "datasource": "MICS",
    },  # 32
    {
        "name": "Percentage of pregnant women tested for HIV during antenatal care -> MICS",
        "indicator": "Percentage of pregnant women tested for HIV during antenatal care",
        "datasource": "MICS",
    },  # 33
    {
        "name": "Percentage of women age 15-49 years who received at least one IPT dose during pregnancy -> MICS",
        "indicator": "Percentage of women age 15-49 years who received at least one IPT dose during pregnancy",
        "datasource": "MICS",
    },  # 34
    {
        "name": "Percentage of women age 15-49 years who received at least two or more IPT doses during pregnancy -> MICS",
        "indicator": "Percentage of women age 15-49 years who received at least two or more IPT doses during pregnancy",
        "datasource": "MICS",
    },  # 35
    {
        "name": "Percentage of women age 15-49 years who received at least two or more IPT doses during pregnancy -> NHMIS",
        "indicator": "Percentage of women age 15-49 years who received at least two or more IPT doses during pregnancy",
        "datasource": "NHMIS",
    },  # 36
    {
        "name": "Postnatal care coverage (mother) -> MICS",
        "indicator": "Postnatal care coverage (mother)",
        "datasource": "MICS",
    },  # 37
    {
        "name": "Prevalence of Symptoms of Acute Respiratory Infection among under five children -> MICS",
        "indicator": "Prevalence of Symptoms of Acute Respiratory Infection among under five children",
        "datasource": "MICS",
    },  # 38
    {
        "name": "Prevalence of children with diarrhoea -> IHME",
        "indicator": "Prevalence of children with diarrhoea",
        "datasource": "IHME",
    },  # 39
    {
        "name": "Prevalence of children with diarrhoea -> KDGHS",
        "indicator": "Prevalence of children with diarrhoea",
        "datasource": "KDGHS",
    },  # 40
    {
        "name": "Prevalence of children with diarrhoea -> MICS",
        "indicator": "Prevalence of children with diarrhoea",
        "datasource": "MICS",
    },  # 41
    {
        "name": "Prevalence of stunting among under 5 children -> IHME",
        "indicator": "Prevalence of stunting among under 5 children",
        "datasource": "IHME",
    },  # 42
    {
        "name": "Prevalence of stunting among under 5 children -> MICS",
        "indicator": "Prevalence of stunting among under 5 children",
        "datasource": "MICS",
    },  # 43
    {
        "name": "Prevalence of wasting among under 5 children -> MICS",
        "indicator": "Prevalence of wasting among under 5 children",
        "datasource": "MICS",
    },  # 45
    {
        "name": "Skilled attendance at delivery or birth -> KDGHS",
        "indicator": "Skilled attendance at delivery or birth",
        "datasource": "KDGHS",
    },  # 46
    {
        "name": "Skilled attendance at delivery or birth -> MICS",
        "indicator": "Skilled attendance at delivery or birth",
        "datasource": "MICS",
    },  # 47
    {
        "name": "Skilled attendance at delivery or birth -> NHMIS",
        "indicator": "Skilled attendance at delivery or birth",
        "datasource": "NHMIS",
    },  # 48
    {
        "name": "Total fertility rate -> MICS",
        "indicator": "Total fertility rate",
        "datasource": "MICS",
    },  # 49
    {
        "name": "Total fertility rate -> NHMIS",
        "indicator": "Total fertility rate",
        "datasource": "NHMIS",
    },  # 50
    {
        "name": "Under 5 Mortality rate -> KDGHS",
        "indicator": "Under 5 Mortality rate",
        "datasource": "KDGHS",
    },  # 51
    {
        "name": "Under 5 Mortality rate -> MICS",
        "indicator": "Under 5 Mortality rate",
        "datasource": "MICS",
    },  # 52
    {
        "name": "Under 5 Mortality rate -> NHMIS",
        "indicator": "Under 5 Mortality rate",
        "datasource": "NHMIS",
    },  # 53
    {
        "name": "Underweight prevalence among under 5 children -> MICS",
        "indicator": "Underweight prevalence among under 5 children",
        "datasource": "MICS",
    },  # 54
    {
        "name": "Underweight prevalence among under 5 children -> NHMIS",
        "indicator": "Underweight prevalence among under 5 children",
        "datasource": "NHMIS",
    },  # 55
    {
        "name": "Unmet need for family planning -> MICS",
        "indicator": "Unmet need for family planning",
        "datasource": "MICS",
    },  # 56
]


def run_process():
    """
    run the data-processing
    """
    # ===================================
    # LOAD OPTIMIZED DATA QUERY CACHES
    # ===================================
    converter_utils.helper_cache_data_processor_refrences()

    # pre populate data-caches
    # NOTE the comments in the data_row population loop
    data_row_structure = []
    data_res_model_fields = []
    for index in range(0, len(response_model)):
        data_row_structure.append("")
        data_res_model_fields.append([])

    response_data = []

    try:
        # ================================
        # RUN QUERIES
        # ================================

        # LGAS
        data_lgas = converter_utils.helper_extract_locations_nigerian_lgas()

        # DATA
        # a single request for all data in the data_table
        data_all = main_models.Data.objects.all().select_related("datasource", "indicator")

        # ================================
        # PARSE QUERY DATA
        # ================================

        # cycle through the response-headers for indicators and datasources that exists
        # for those that exist cycle throuh the data for their data-value in the database
        # and add to the list of data_res_model_fields
        converter_utils.helper_populate_indicator_datasource_field(
            data_res_model_fields, response_model, data_all
        )

        # ================================
        # PACKAGE RESPONSE
        # ================================

        # CREATE THE FIRST data_item
        data_headings = []
        for heading in response_model:
            data_headings.append(heading["name"])
        response_data.append(data_headings)

        # CREATE THE rows
        for period in range(PERIOD["start"], PERIOD["end"]):
            for lga in data_lgas:
                # shallow copy the initialized list structure
                data_row = data_row_structure.copy()

                # index 0
                data_row[0] = period
                # index 1
                # state name(state is parent of lga)
                data_row[1] = converter_utils.helper_get_location_by_id(lga.parent).name
                # index 2
                # lga name
                data_row[2] = lga.name

                for index in range(3, len(data_row)):  # index 3-56
                    data_row[index] = (
                        converter_utils.helper_extract_data_value_by_location_and_period(
                            data_res_model_fields[index], period, lga.id
                        )
                    )

                response_data.append(data_row)

        return response_data

    except Exception as e:
        # LOG
        utils_logger.log_print("", str(e), param_oneline=True)

        return response_data
