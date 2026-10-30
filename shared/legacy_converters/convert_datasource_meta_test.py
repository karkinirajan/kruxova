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
    {"name": "Data source"},  # 0
    {"name": "Full name"},  # 1
    {"name": "Description"},  # 2
    {"name": "Years with available data"},  # 3
    {"name": "Next period of available dataset"},  # 4
    {"name": "Link"},  # 5
    {"name": "Methodology"},  # 6
    {"name": "Subnational data available?"},  # 7
    {"name": "Classification"},  # 8
]


def helper_get_datasource_links(param_data_links, param_datasource_id):
    data = []
    for link in param_data_links:
        if link.datasource_id == param_datasource_id:
            data.append(link)
    return data


def run_process():
    """
    run the data-processing
    """
    # ===================================
    # LOAD OPTIMIZED DATA QUERY CACHES
    # ===================================
    converter_utils.helper_cache_data_processor_refrences()

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
        data_datasources = main_models.Datasource.objects.all()

        # LINKS
        data_links = main_models.Link.objects.all()

        # ================================
        # PACKAGE RESPONSE
        # ================================

        # CREATE THE FIRST data_item
        data_headings = []
        for heading in response_model:
            data_headings.append(heading["name"])
        response_data.append(data_headings)

        # CREATE THE rows
        for datasource in data_datasources:
            datasource_links = helper_get_datasource_links(data_links, datasource.id)

            data_row = data_row_structure.copy()

            data_row[0] = datasource.datasource
            data_row[1] = datasource.full_name
            data_row[2] = datasource.description
            data_row[3] = datasource.year_available if datasource.year_available is not None else ""
            data_row[4] = datasource.period_available

            links_comma_seperated = ""
            if len(datasource_links) != 0:
                for link in datasource_links:
                    links_with_period = str(link.period) + " " + link.link

                    # first cantencation when the value is empty
                    if links_comma_seperated != "":
                        links_comma_seperated = links_comma_seperated + "," + links_with_period
                    else:
                        links_comma_seperated = links_with_period

            data_row[5] = links_comma_seperated

            data_row[6] = datasource.methodology
            data_row[7] = (
                datasource.subnational_data if datasource.subnational_data is not None else ""
            )
            data_row[8] = datasource.classification if datasource.classification is not None else ""

            response_data.append(data_row)

        # LOG
        # utils_logger.log_print("RESPONSE DATA",response_data,param_oneline=False)

        return response_data

    except Exception as e:
        # LOG
        utils_logger.log_print("", str(e), param_oneline=True)

        return response_data
