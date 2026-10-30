# *****************************************
# IMPORTs python
# *****************************************

# *****************************************
# IMPORTs django
# *****************************************

# *****************************************
# IMPORTs app
# *****************************************
from apps.main.api_routes.api_routes_crud import api_routes_crud_viewsets


def register_routes(param_global_router):
    """
    register the routes with a(the) single global router

    Args:
        :param param_global_router: the global drf router object
    Returns:
        :rtype:void
    """

    # ********************************************************************************
    # APP_MAIN MODELS CRUD(DEFAULT) ROUTES
    # ********************************************************************************

    param_global_router.register(r"group", api_routes_crud_viewsets.GroupViewSet, "Group")

    param_global_router.register(r"location", api_routes_crud_viewsets.LocationViewSet, "Location")

    param_global_router.register(
        r"location_hierarchy_level",
        api_routes_crud_viewsets.LocationHierarchyLevelViewSet,
        "LocationHierarchyLevel",
    )

    param_global_router.register(
        r"valuetypes", api_routes_crud_viewsets.ValueTypeViewSet, "ValueTypes"
    )

    param_global_router.register(r"factors", api_routes_crud_viewsets.FactorViewSet, "Factors")

    param_global_router.register(
        r"datasources", api_routes_crud_viewsets.DatasourceViewSet, "Datasources"
    )

    param_global_router.register(
        r"datasource_valuetypes",
        api_routes_crud_viewsets.DatasourceValuetypeViewSet,
        "DatasourceValuetypes",
    )

    param_global_router.register(
        r"datasource_locations",
        api_routes_crud_viewsets.DatasourceLocationViewSet,
        "DatasourceLocations",
    )

    param_global_router.register(
        r"datasource_specific_indicator",
        api_routes_crud_viewsets.DatasourceSpecificIndicatorViewSet,
        "DatasourceSpecificIndicator",
    )

    param_global_router.register(
        r"indicators", api_routes_crud_viewsets.IndicatorViewSet, "Indicators"
    )

    param_global_router.register(
        r"indicator_valuetypes",
        api_routes_crud_viewsets.IndicatorValuetypeViewSet,
        "IndicatorValuetypes",
    )

    param_global_router.register(r"links", api_routes_crud_viewsets.LinkViewSet, "Links")

    param_global_router.register(r"data", api_routes_crud_viewsets.DataViewSet, "Data")

    param_global_router.register(
        r"subscriber", api_routes_crud_viewsets.SubscriberViewSet, "Subscriber"
    )

    param_global_router.register(r"user", api_routes_crud_viewsets.UserViewSet, "User")
    param_global_router.register(
        r"dashobard", api_routes_crud_viewsets.DashboardViewSet, "Dashboard"
    )
