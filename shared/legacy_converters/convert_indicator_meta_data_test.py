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

response_model = [
    {"name": "Data Source"},  # 0
    {"name": "Generalized indicator name"},  # 1
    {"name": "Data source indicator name"},  # 2
    {"name": "Measurement(Numerator)"},  # 3
    {"name": "Measurement(Denominator)"},  # 4
    {"name": "Frequency"},  # 5
    {"name": "Methodology (Method of estimation)"},  # 6
    {"name": "Indicator definition"},  # 7
    {"name": "Level of data available"},  # 8
    {"name": "Available data - source/period"},  # 9
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
    data_row_structure = []
    for index in range(0, len(response_model)):
        data_row_structure.append("")
    response_data = []

    try:
        # ================================
        # RUN QUERIES
        # ================================

        # DATASOURCE_INDICATORS
        data_datasources_indicators = main_models.DatasourceSpecificIndicator.objects.all()

        # ================================
        # PACKAGE RESPONSE
        # ================================

        # CREATE THE FIRST data_item
        data_headings = []
        for heading in response_model:
            data_headings.append(heading["name"])
        response_data.append(data_headings)

        # CREATE THE rows
        for data_item in data_datasources_indicators:
            # shallow copy the initialized list structure
            data_row = data_row_structure.copy()

            data_row[0] = data_item.datasource.datasource

            data_row[1] = data_item.indicator.full_name

            data_row[2] = data_item.datasource_indicator

            data_row[3] = data_item.measurement_numerator

            data_row[4] = data_item.measurement_denominator

            data_row[5] = data_item.frequency

            data_row[6] = data_item.methodology_estimation

            data_row[7] = data_item.indicator_definition

            data_row[8] = data_item.data_level

            data_row[9] = ""

            response_data.append(data_row)

        # LOG
        # utils_logger.log_print("RESPONSE DATA",response_data,param_oneline=False)

        return response_data

    except Exception as e:
        # LOG
        utils_logger.log_print("", str(e), param_oneline=True)

        return response_data
