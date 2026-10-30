# ********************
# imports django
# ********************
from apps.main import models

# ********************
# imports shared
# ********************
from shared.utils import utils_logger

LOCATION_NAME_COUNTRY_NIGERIA = "Nigeria"
LOCATION_HEIRARCHY_NAME_COUNTRY = "Countries"
LOCATION_HEIRARCHY_NAME_STATES = "States"
LOCATION_HEIRARCHY_NAME_ZONES = "Zones"
LOCATION_HEIRARCHY_NAME_LGAS = "LGAs"

LOCATION_HEIRARCHY_ID_STATES = 3
LOCATION_HEIRARCHY_ID_LGAS = 4

CACHE_INDICATORS_BY_NAME = None
CACHE_DATASOURCES_BY_NAME = None
CACHE_LOCATIONS_BY_ID = None
CACHE_LOCATIONS_LIST = None


def helper_cache_data_processor_refrences():
    """
    make unlazy query for indicators and datasources
    process into a dict to cache in a global var

    Args:
        Void
    Returns:
        Void
    """
    global CACHE_INDICATORS_BY_NAME
    global CACHE_DATASOURCES_BY_NAME
    global CACHE_LOCATIONS_BY_ID
    global CACHE_LOCATIONS_LIST

    if CACHE_DATASOURCES_BY_NAME is None and CACHE_INDICATORS_BY_NAME is None:
        utils_logger.print_prety(
            "CACHING REFRENCES",
            "the data proccessing refrences are NONE caching now",
            param_oneline=False,
        )

        # INDICATORS
        CACHE_INDICATORS_BY_NAME = {}

        temp_data_indicator = models.Indicator.objects.all().values()

        for indic in temp_data_indicator:
            CACHE_INDICATORS_BY_NAME[indic["full_name"]] = indic["id"]

        # DATASOURCES
        CACHE_DATASOURCES_BY_NAME = {}

        temp_data_datasources = models.Datasource.objects.all().values()

        for source in temp_data_datasources:
            CACHE_DATASOURCES_BY_NAME[source["datasource"]] = source["id"]

        # LOCATIONS
        CACHE_LOCATIONS_BY_ID = {}

        temp_data_locations = models.Location.objects.all()

        for location in temp_data_locations:
            CACHE_LOCATIONS_BY_ID[location.id] = location

        CACHE_LOCATIONS_LIST = temp_data_locations


def helper_populate_indicator_datasource_field(
    param_response_model_list,  # refrence to variable defined in the route
    param_response_model,
    param_data,
):
    """
    fill the pre-populated model_list with data
    cycle through the response-headers for indicators and datasources that exists
    for those that exist cycle throuh the data for their data-value in the database
    and add to the list of data_res_model_fields

    Args:
        :param param_response_model_list: the pre-populated structure list of the response model
        :param param_response_model: the response model
        :param_data: the retrieved data
    Returns:
        :rtype: void
    """

    response_model_list = param_response_model_list

    utils_logger.log_print("CACHE_INDICATORS", CACHE_INDICATORS_BY_NAME, param_oneline=False)
    utils_logger.log_print("CACHE_DATASOURCES", CACHE_DATASOURCES_BY_NAME, param_oneline=False)

    # cycle through the response-headers for indicators and datasources that exists
    # first-list of the response
    for response_field_index, response_field in enumerate(param_response_model):
        if (param_response_model[response_field_index]["indicator"] != "") and (
            param_response_model[response_field_index]["datasource"] != ""
        ):
            if (
                param_response_model[response_field_index]["indicator"] in CACHE_INDICATORS_BY_NAME
            ) and (
                param_response_model[response_field_index]["datasource"]
                in CACHE_DATASOURCES_BY_NAME
            ):
                for data_item in param_data:
                    if (
                        data_item.indicator_id
                        == CACHE_INDICATORS_BY_NAME[
                            param_response_model[response_field_index]["indicator"]
                        ]
                    ) and (
                        data_item.datasource_id
                        == CACHE_DATASOURCES_BY_NAME[
                            param_response_model[response_field_index]["datasource"]
                        ]
                    ):
                        response_model_list[response_field_index].append(data_item)
            else:
                if (
                    param_response_model[response_field_index]["indicator"]
                    in CACHE_INDICATORS_BY_NAME
                ):
                    # LOG
                    utils_logger.log_print(
                        "RESPONSE_MODEL_HEADER_INDEX->{} INDICATOR NOT EXIST".format(
                            response_field_index
                        ),
                        response_field,
                        param_oneline=False,
                    )
                if (
                    param_response_model[response_field_index]["datasource"]
                    in CACHE_DATASOURCES_BY_NAME
                ):
                    # LOG
                    utils_logger.log_print(
                        "RESPONSE_MODEL_HEADER_INDEX->{} DATASOURCE NOT EXIST".format(
                            response_field_index
                        ),
                        response_field,
                        param_oneline=False,
                    )
        else:
            utils_logger.log_print(
                "RESPONSE_MODEL_HEADER_INDEX->{} DATASOURCE AND INDICATOR NOT EXIST".format(
                    response_field_index
                ),
                response_field,
                param_oneline=False,
            )


def helper_extract_data_value_by_location_and_period(param_data, param_period, param_location_id):
    """
    from data retrieved by indicator_id and datasource_id
    get the data.value of a row with a mathing period with the location_id=a country_id
    due to location_level being equal to Countries

    Args:
        :param param_data: the queryset list of data
        :param param_period: the year
        :param param_location_id: the country
    Returns:
        :rtype:int
    """
    data = ""
    if param_data is not None:
        for item in param_data:
            if (int(item.period) == int(param_period)) and (
                int(item.location_id) == int(param_location_id)
            ):
                if item.value is not None:
                    data = float(item.value)
                    # LOG
                    utils_logger.log_print(
                        "DATA AVAILABLE : LOCATION_ID-> {} PERIOD-> {}".format(
                            param_location_id, param_period
                        ),
                        item,
                        param_oneline=False,
                    )
    return data


def helper_get_location_by_id(param_id):
    return CACHE_LOCATIONS_BY_ID[param_id]


def helper_get_location_country_nigeria():
    return models.Location.objects.get(name=LOCATION_NAME_COUNTRY_NIGERIA)


def helper_extract_locations_nigerian_states():
    """
    get nigerian states location_data

    Args:
    Returns:
        :rtype:[]
    """

    data_states = []

    """
    data_location_nigeria=models.Location.objects.\
        filter(name=LOCATION_NAME_COUNTRY_NIGERIA)

    data_location_level_state=models.LocationHierarchyLevel.objects.\
        filter(name=LOCATION_HEIRARCHY_NAME_STATES)[0]

    for location in CACHE_LOCATIONS_LIST:
        if (location.level==data_location_level_state.id):
            #get parent(zone) location data by parent_id
            state_zone=CACHE_LOCATIONS_BY_ID[location.parent]
            
            #check if zone.parent_id is that of nigeria
            if CACHE_LOCATIONS_BY_ID[state_zone.parent].id==data_location_nigeria.id:
                data_states.append(location)
    """

    # simplified for when only nigeria data in tables
    for location in CACHE_LOCATIONS_LIST:
        if location.level_id == LOCATION_HEIRARCHY_ID_STATES:
            data_states.append(location)

    return data_states


def helper_extract_locations_nigerian_lgas():
    """
    get nigerian lga location_data

    Args:
    Returns:
        :rtype:[]
    """

    data_lgas = []

    """
    data_location_nigeria=models.Location.objects.\
        filter(name=LOCATION_NAME_COUNTRY_NIGERIA)

    data_location_level_zone=models.LocationHierarchyLevel.objects.\
        filter(name=LOCATION_HEIRARCHY_NAME_ZONES)[0]

    data_location_level_lga=models.LocationHierarchyLevel.objects.\
        filter(name=LOCATION_HEIRARCHY_NAME_LGAS)[0]

    for location in CACHE_LOCATIONS_LIST:
        if (location.level==data_location_level_lga.id):
            lga_state=CACHE_LOCATIONS_BY_ID[location.parent]
            
            if CACHE_LOCATIONS_BY_ID[lga_state.parent].level==data_location_level_zone.id:
                state_zone=CACHE_LOCATIONS_BY_ID[lga_state.parent]

                if CACHE_LOCATIONS_BY_ID[state_zone.parent].id==data_location_nigeria.id:
                    data_lgas.append(location)

    """

    # simplified for when only nigeria data in tables
    for location in CACHE_LOCATIONS_LIST:
        if location.level_id == LOCATION_HEIRARCHY_ID_LGAS:
            data_lgas.append(location)

    return data_lgas
