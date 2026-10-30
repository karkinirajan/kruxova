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

COUNTRY_ID_NIGERIA = 1

PERIOD_NATIONAL = {"start": 1964, "end": 1990}
PERIOD_STATES = {"start": 1990, "end": 2019}

response_model = [
    {"name": "Period", "indicator": "", "datasource": ""},  # 0
    {"name": "State", "indicator": "", "datasource": ""},  # 1
    {
        "name": "ANC Coverage (at least 1 visit) -> NNHS",
        "indicator": "ANC Coverage (at least 1 visit)",
        "datasource": "NNHS",
    },  # 2 test with MICS
    {
        "name": "Adolescent birth rate -> IHME",
        "indicator": "Adolescent birth rate",
        "datasource": "IHME",
    },  # 3
    {
        "name": "Contraceptive prevalence rate -> NNHS",
        "indicator": "Contraceptive prevalence rate",
        "datasource": "NNHS",
    },  # 4
    {
        "name": "DPT 3/Penta 3 coverage rate -> IHME",
        "indicator": "DPT 3/Penta 3 coverage rate",
        "datasource": "IHME",
    },  # 5
    {
        "name": "DPT 3/Penta 3 coverage rate -> NNHS",
        "indicator": "DPT 3/Penta 3 coverage rate",
        "datasource": "NNHS",
    },  # 6
    {
        "name": "IPV coverage rate -> IHME",
        "indicator": "IPV coverage rate",
        "datasource": "IHME",
    },  # 7
    {
        "name": "Infant Mortality rate -> WHO-GHO",
        "indicator": "Infant Mortality rate",
        "datasource": "WHO-GHO",
    },  # 8
    {
        "name": "Infant Mortality rate -> World Bank",
        "indicator": "Infant Mortality rate",
        "datasource": "World Bank",
    },  # 9
    {
        "name": "Maternal Mortality Ratio -> IHME",
        "indicator": "Maternal Mortality Ratio",
        "datasource": "IHME",
    },  # 10
    {
        "name": "Maternal Mortality Ratio -> WHO-GHO",
        "indicator": "Maternal Mortality Ratio",
        "datasource": "WHO-GHO",
    },  # 11
    {
        "name": "Measles Immunization Coverage -> IHME",
        "indicator": "Measles Immunization Coverage",
        "datasource": "IHME",
    },  # 12
    {
        "name": "Measles Immunization Coverage -> NNHS",
        "indicator": "Measles Immunization Coverage",
        "datasource": "NNHS",
    },  # 13
    {
        "name": "Neonatal mortality rate (per 1000 live births) -> IHME",
        "indicator": "Neonatal mortality rate (per 1000 live births)",
        "datasource": "IHME",
    },  # 14
    {
        "name": "Neonatal mortality rate (per 1000 live births) -> WHO-GHO",
        "indicator": "Neonatal mortality rate (per 1000 live births)",
        "datasource": "WHO-GHO",
    },  # 15
    {
        "name": "Neonatal mortality rate (per 1000 live births) -> World Bank",
        "indicator": "Neonatal mortality rate (per 1000 live births)",
        "datasource": "World Bank",
    },  # 16
    {
        "name": "Percentage of children under 5 with fever who received ACT -> NNHS",
        "indicator": "Percentage of children under 5 with fever who received ACT",
        "datasource": "NNHS",
    },  # 17
    {
        "name": "Percentage of children under 6 months who were exclusively breastfed -> IHME",
        "indicator": "Percentage of children under 6 months who were exclusively breastfed",
        "datasource": "IHME",
    },  # 18
    {
        "name": "Percentage of children under 6 months who were exclusively breastfed -> NNHS",
        "indicator": "Percentage of children under 6 months who were exclusively breastfed",
        "datasource": "NNHS",
    },  # 19
    {
        "name": "Percentage of children with diarrhoea who received treatment -> NNHS",
        "indicator": "Percentage of children with diarrhoea who received treatment",
        "datasource": "NNHS",
    },  # 20
    {
        "name": "Percentage of pregnant women tested for HIV during antenatal care -> NNHS",
        "indicator": "Percentage of pregnant women tested for HIV during antenatal care",
        "datasource": "NNHS",
    },  # 21
    {
        "name": "Percentage of women age 15-49 years who received at least one IPT dose during pregnancy -> NNHS",
        "indicator": "Percentage of women age 15-49 years who received at least one IPT dose during pregnancy",
        "datasource": "NNHS",
    },  # 22
    {
        "name": "Prevalence of HIV -> UNAIDS",
        "indicator": "Prevalence of HIV",
        "datasource": "UNAIDS",
    },  # 23
    {
        "name": "Prevalence of HIV -> WHO-GHO",
        "indicator": "Prevalence of HIV",
        "datasource": "WHO-GHO",
    },  # 24
    {
        "name": "Prevalence of Symptoms of Acute Respiratory Infection among under five children -> NNHS",
        "indicator": "Prevalence of Symptoms of Acute Respiratory Infection among under five children",
        "datasource": "NNHS",
    },  # 25
    {
        "name": "Prevalence of children with diarrhoea -> IHME",
        "indicator": "Prevalence of children with diarrhoea",
        "datasource": "IHME",
    },  # 25
    {
        "name": "Prevalence of children with diarrhoea -> NNHS",
        "indicator": "Prevalence of children with diarrhoea",
        "datasource": "NNHS",
    },  # 26
    {
        "name": "Prevalence of malaria among under five children (microscopy positive) -> IHME",
        "indicator": "Prevalence of malaria among under five children (microscopy positive)",
        "datasource": "IHME",
    },  # 28
    {
        "name": "Prevalence of stunting among under 5 children -> IHME",
        "indicator": "Prevalence of stunting among under 5 children",
        "datasource": "IHME",
    },  # 29
    {
        "name": "Prevalence of stunting among under 5 children -> NNHS",
        "indicator": "Prevalence of stunting among under 5 children",
        "datasource": "NNHS",
    },  # 30
    {
        "name": "Prevalence of wasting among under 5 children -> IHME",
        "indicator": "Prevalence of wasting among under 5 children",
        "datasource": "IHME",
    },  # 31
    {
        "name": "Prevalence of wasting among under 5 children -> NNHS",
        "indicator": "Prevalence of wasting among under 5 children",
        "datasource": "NNHS",
    },  # 32
    {
        "name": "Proportion of children under 5 with ARI who received antibiotics -> NNHS",
        "indicator": "Proportion of children under 5 with ARI who received antibiotics",
        "datasource": "NNHS",
    },  # 33
    {
        "name": "Skilled attendance at delivery or birth -> IHME",
        "indicator": "Skilled attendance at delivery or birth",
        "datasource": "IHME",
    },  # 34
    {
        "name": "Skilled attendance at delivery or birth -> NNHS",
        "indicator": "Skilled attendance at delivery or birth",
        "datasource": "NNHS",
    },  # 35
    {
        "name": "Total fertility rate -> IHME",
        "indicator": "Total fertility rate",
        "datasource": "IHME",
    },  # 36
    {
        "name": "Under 5 Mortality rate -> IHME",
        "indicator": "Under 5 Mortality rate",
        "datasource": "IHME",
    },  # 37
    {
        "name": "Under 5 Mortality rate -> WHO-GHO",
        "indicator": "Under 5 Mortality rate",
        "datasource": "WHO-GHO",
    },  # 38
    {
        "name": "Under 5 Mortality rate -> World Bank",
        "indicator": "Under 5 Mortality rate",
        "datasource": "World Bank",
    },  # 39
    {
        "name": "Underweight prevalence among under 5 children -> IHME",
        "indicator": "Underweight prevalence among under 5 children",
        "datasource": "IHME",
    },  # 40
    {
        "name": "Underweight prevalence among under 5 children -> NNHS",
        "indicator": "Underweight prevalence among under 5 children",
        "datasource": "NNHS",
    },  # 41
    {
        "name": "Vitamin A supplementation coverage -> NNHS",
        "indicator": "Vitamin A supplementation coverage",
        "datasource": "NNHS",
    },  # 42
]


def run_process():
    """
    run the data-processing
    """
    # ===================================
    # LOAD OPTIMIZED DATA QUERY CACHES
    # ===================================
    converter_utils.helper_cache_data_processor_refrences()

    # the response data to be serialized
    data_row_structure = []

    # the proccesing temp data-cache
    data_res_model_fields = []

    # pre populate data-caches
    # initialize the the lists structure
    for index in range(0, len(response_model)):
        data_row_structure.append("")
        data_res_model_fields.append([])

    response_data = []

    try:
        # ================================
        # RUN QUERIES
        # ================================

        # LOCATIONS
        data_location_states = converter_utils.helper_extract_locations_nigerian_lgas()

        # DATA
        # a single request for all data in the data_table
        data_all = main_models.Data.objects.filter(value_type__id=1).select_related(
            "datasource", "indicator"
        )

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

        def func_create_rows_for_national_data_within_a_period(param_period):
            """
            create rows of data.state_id=1(nigeria),location_level=1(countries),country=1(nigeria)

            Args:
                :param param_period:int
            Returns:
                :rtype: Void
            """
            # shallow copy the initialized list structure
            data_row = data_row_structure.copy()

            data_row[0] = period  # index 0
            data_row[1] = "National"  # index 1

            for index in range(2, len(data_row)):  # index 2 to 42
                data_row[index] = converter_utils.helper_extract_data_value_by_location_and_period(
                    data_res_model_fields[index], param_period, COUNTRY_ID_NIGERIA
                )

            response_data.append(data_row)

        def func_create_rows_for_state_within_a_period(param_period):
            """
            create rows of data.state_id=1 in the period range

            Args:
                :param param_period:int
            Returns:
                :rtype: Void
            """

            for state in data_location_states:
                # shallow copy the initialized list structure
                data_row = data_row_structure.copy()

                data_row[0] = period  # index 0
                data_row[1] = state.name  # index 1

                for index in range(2, len(data_row)):  # index 2-42
                    data_row[index] = (
                        converter_utils.helper_extract_data_value_by_location_and_period(
                            data_res_model_fields[index], param_period, state.id
                        )
                    )

                response_data.append(data_row)

        # CREATE THE rows for national-level-data from 1964 to 1989
        for period in range(PERIOD_NATIONAL["start"], PERIOD_NATIONAL["end"]):
            func_create_rows_for_national_data_within_a_period(period)

        # CREATE THE rows for location-level-data from 1990 to
        for period in range(PERIOD_STATES["start"], PERIOD_STATES["end"]):
            func_create_rows_for_national_data_within_a_period(period)

            func_create_rows_for_state_within_a_period(period)

        return response_data

    except Exception as e:
        # LOG
        utils_logger.log_print("", str(e), param_oneline=True)

        return response_data
