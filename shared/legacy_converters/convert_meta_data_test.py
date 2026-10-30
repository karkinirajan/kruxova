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

# ********************
# imports app
# ********************
from apps.main import models as main_models

response_model = [
    {"name": "Generalized indicator name"},  # 0
    {"name": "Generalized Indicator Short name"},  # 1
    {"name": "Multiplier factor"},  # 2
    {"name": "Display factor"},  # 3
    {"name": "Desirable slope"},  # 4
    {"name": "Type of Indicator"},  # 5
    {"name": "Program Area"},  # 6
    {"name": "National Target"},  # 7
    {"name": "Source document for National Target"},  # 8
    {"name": "Information about National Target Source Document"},  # 9
    {"name": "SDG target"},  # 10
    {"name": "Information about SDG Target Source Document"},  # 11
    {"name": "1st related indicator"},  # 12
    {"name": "2nd related indicator"},  # 13
    {"name": "3rd related indicator"},  # 14
    {"name": "4th related indicator"},  # 15
    {"name": "created_on"},  # 16
]


def run_process():
    """
    run the data-processing
    """

    # converter_utils.helper_cache_data_processor_refrences()

    # pre populate data-caches
    # initialize the the list
    data_row_structure = []
    for index in range(0, len(response_model)):
        data_row_structure.append("")
    response_data = []

    try:
        # ================================
        # RUN QUERIES
        # ================================

        # INDICATORS
        data_indicators = main_models.Indicator.objects.all().select_related("factor")

        # ================================
        # PACKAGE RESPONSE
        # ================================

        # CREATE THE FIRST data_item
        data_headings = []
        for heading in response_model:
            data_headings.append(heading["name"])
        response_data.append(data_headings)

        # use non-self-referencing fields to extract details
        indicators_map_id_to_fullname = {}
        for indicator in data_indicators:
            indicators_map_id_to_fullname[indicator.id] = indicator.full_name

        # CREATE THE rows
        for indicator in data_indicators:
            # shallow copy the initialized list structure
            data_row = data_row_structure.copy()

            # extract relation factor
            indicator_factor = indicator.factor

            # response fields

            data_row[0] = indicator.full_name

            data_row[1] = indicator.short_name

            data_row[2] = (
                float(indicator_factor.multiplier_factor) if indicator_factor is not None else ""
            )

            data_row[3] = indicator_factor.display_factor if indicator_factor is not None else ""

            data_row[4] = indicator.desirable_slope

            data_row[5] = indicator.indicator_type

            data_row[6] = indicator.program_area

            data_row[7] = (
                float(indicator.national_target) if indicator.national_target is not None else ""
            )

            data_row[8] = indicator.national_source if indicator.national_source is not None else ""

            data_row[9] = (
                indicator.national_information if indicator.national_information is not None else ""
            )

            data_row[10] = indicator.sdg_target if indicator.sdg_target is not None else ""

            data_row[11] = (
                indicator.sdg_information if indicator.sdg_information is not None else ""
            )

            data_row[12] = (
                indicators_map_id_to_fullname[int(indicator.first_related)]
                if indicator.first_related is not None
                else ""
            )

            data_row[13] = (
                indicators_map_id_to_fullname[int(indicator.second_related)]
                if indicator.second_related is not None
                else ""
            )

            data_row[14] = (
                indicators_map_id_to_fullname[int(indicator.third_related)]
                if indicator.third_related is not None
                else ""
            )

            data_row[15] = (
                indicators_map_id_to_fullname[int(indicator.fourth_related)]
                if indicator.fourth_related is not None
                else ""
            )

            data_row[16] = indicator.created_at if indicator.created_at is not None else ""

            response_data.append(data_row)

        # LOG
        # utils_logger.log_print("RESPONSE DATA",response_data,param_oneline=False)

        return response_data

    except Exception as e:
        # LOG
        utils_logger.log_print("", str(e), param_oneline=True)

        return response_data
