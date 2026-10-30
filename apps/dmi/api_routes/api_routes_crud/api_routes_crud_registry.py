# *****************************************
# IMPORTs python
# *****************************************

# *****************************************
# IMPORTs django
# *****************************************

# *****************************************
# IMPORTs app
# *****************************************
from apps.dmi.api_routes.api_routes_crud import api_routes_crud_viewsets


def register_routes(param_global_router):
    """
    register the routes with a(the) single global router

    Args:
        :param param_global_router: the global drf router object
    Returns:
        :rtype:void
    """
    param_global_router.register(r"data", api_routes_crud_viewsets.DataViewSet, "Data")
