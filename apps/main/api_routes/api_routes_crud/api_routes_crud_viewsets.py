# *****************************************
# IMPORTs python
# *****************************************

# *****************************************
# IMPORTs django
# *****************************************
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.response import Response
from django.db import connection
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.decorators import action

# *****************************************
# IMPORTs app
# *****************************************
# settings

# models
from apps.main import models as main_models

# serializers
from apps.main.api_routes.api_routes_crud import api_routes_crud_serializers
from drf_yasg.utils import swagger_auto_schema


class CustomModelViewSet(viewsets.ModelViewSet):
    """
    extention to provide default custom overrides for actions
    """

    permission_classes = (IsAuthenticatedOrReadOnly,)

    # DISABLE DELETE-METHOD if the deployed env is production
    # def destroy(self, request, pk=None):
    #    if utils.helper_check_env_is_pro():
    #        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    #    elif utils.helper_check_env_is_local():
    #        return super().destroy(request,pk)
    #    else:
    #        return super().destroy(request,pk)


# ********************************************************************************
# APP_MAIN MODELS CRUD(DEFAULT) VIEWSETS
# ********************************************************************************

UserModel = get_user_model()


class UserViewSet(CustomModelViewSet):
    # account management is staff-only: reads were public and returned password hashes, and any
    # token holder could overwrite another user's password
    permission_classes = (IsAdminUser,)
    serializer_class = api_routes_crud_serializers.UserSerializer
    queryset = UserModel.objects.all()


class GroupViewSet(CustomModelViewSet):
    serializer_class = api_routes_crud_serializers.GroupSerializer
    queryset = main_models.Group.objects.all()

    # # Implement CACHING on dispatch function to add caching to all endpoints
    # @method_decorator(cache_page(60 * 60 * 2))
    # def dispatch(self, request, *args, **kwargs):
    #     return super().dispatch(request, *args, **kwargs)


class LocationViewSet(CustomModelViewSet):
    serializer_class = api_routes_crud_serializers.LocationSerializer
    queryset = main_models.Location.objects.select_related("level")

    # # Implement CACHING on dispatch function to add caching to all endpoints
    # @method_decorator(cache_page(60 * 60 * 2))
    # def dispatch(self, request, *args, **kwargs):
    #     return super().dispatch(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        print("Queries counted {}".format(len(connection.queries)))
        return response


class LocationHierarchyLevelViewSet(CustomModelViewSet):
    serializer_class = api_routes_crud_serializers.LocationHierarchyLevelSerializer
    queryset = main_models.LocationHierarchyLevel.objects.all()

    # # Implement CACHING on dispatch function to add caching to all endpoints
    # @method_decorator(cache_page(60 * 60 * 2))
    # def dispatch(self, request, *args, **kwargs):
    #     return super().dispatch(request, *args, **kwargs)


class ValueTypeViewSet(CustomModelViewSet):
    serializer_class = api_routes_crud_serializers.ValueTypeSerializer
    queryset = main_models.ValueType.objects.all()

    # # Implement CACHING on dispatch function to add caching to all endpoints
    # @method_decorator(cache_page(60 * 60 * 2))
    # def dispatch(self, request, *args, **kwargs):
    #     return super().dispatch(request, *args, **kwargs)


class FactorViewSet(CustomModelViewSet):
    serializer_class = api_routes_crud_serializers.FactorSerializer
    queryset = main_models.Factor.objects.all()

    # # Implement CACHING on dispatch function to add caching to all endpoints
    # @method_decorator(cache_page(60 * 60 * 2))
    # def dispatch(self, request, *args, **kwargs):
    #     return super().dispatch(request, *args, **kwargs)


class DatasourceViewSet(CustomModelViewSet):
    serializer_class = api_routes_crud_serializers.DatasourceSerializer
    queryset = main_models.Datasource.objects.prefetch_related("group")
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["group"]

    # # Implement CACHING on dispatch function to add caching to all endpoints
    # @method_decorator(cache_page(60 * 60 * 2))
    # def dispatch(self, request, *args, **kwargs):
    #     return super().dispatch(request, *args, **kwargs)

    @action(methods=["GET"], detail=True)
    def years_available(self, request, pk, *args, **kwargs):
        """
        This is a custom endpoint to get all the years of data available for
        a particular datasources
        """
        # get the datasources with the specified id
        try:
            datasource = main_models.Datasource.objects.get(id=pk)

        except Exception:
            return Response({"details": "No datasource with the specified id found"}, 400)

        # store all the years of data from that datasource
        years = set()

        # get all the data entries that use that datasource
        entries = main_models.Data.objects.filter(datasource=datasource)

        # get all the years from those entries
        for entry in entries:
            # get the period and add it to the years set
            years.add(entry.period[:4])

        # convert the set of years into a list
        years = list(years)

        # sort the years list from smallest to largest
        years = sorted(years)

        # convert all the years in the list back to strings
        for i in range(len(years)):
            years[i] = str(years[i])

        # reverse the sorted list so it goes from largest to smallest and remove duplicates
        years = reversed(years)

        # return the set of years
        return Response({"years": years}, 200)

    @action(methods=["GET"], detail=True)
    def indicators(self, request, pk, *args, **kwargs):
        """
        This endpiont returns all the available datasources for a specified indicator
        """
        try:
            datasource = main_models.Datasource.objects.get(id=pk)
        except Exception:
            return Response({"detail": "Indicator not found"}, status=404)

        serializer = api_routes_crud_serializers.IndicatorSerializer(
            datasource.indicators.all(), many=True
        )
        return Response(
            {
                "indicators": serializer.data,
            },
            200,
        )


class DatasourceValuetypeViewSet(CustomModelViewSet):
    serializer_class = api_routes_crud_serializers.DatasourceValuetypeSerializer
    queryset = main_models.DatasourceValuetype.objects.all()


class DatasourceLocationViewSet(CustomModelViewSet):
    serializer_class = api_routes_crud_serializers.DatasourceLocationSerializer
    queryset = main_models.DatasourceLocation.objects.all()


class DatasourceSpecificIndicatorViewSet(CustomModelViewSet):
    serializer_class = api_routes_crud_serializers.DatasourceSpecificIndicatorSerializer
    queryset = main_models.DatasourceSpecificIndicator.objects.select_related(
        "datasource", "indicator"
    )


class IndicatorViewSet(CustomModelViewSet):
    serializer_class = api_routes_crud_serializers.IndicatorSerializer
    queryset = main_models.Indicator.objects.select_related("factor").prefetch_related(
        "datasources", "group"
    )
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["group"]

    @action(methods=["GET"], detail=True)
    def datasources(self, request, pk, *args, **kwargs):
        """
        This endpiont returns all the available datasources for a specified indicator
        """
        try:
            indicator = main_models.Indicator.objects.get(id=pk)
        except Exception:
            return Response({"detail": "Indicator not found"}, status=404)

        serializer = api_routes_crud_serializers.DatasourceSerializer(
            indicator.datasources.all(), many=True
        )
        return Response(
            {
                "datasources": serializer.data,
            },
            200,
        )

    @action(methods=["GET"], detail=True)
    def years_available(self, request, pk, *args, **kwargs):
        """
        This is a custom endpoint to get all the years of data available for
        a particular indicator
        """
        # get the indicator with the specified id
        try:
            indicator = main_models.Indicator.objects.get(id=pk)

        except Exception:
            return Response({"details": "No indicator with the specified id found"}, 400)

        # store all the years of data from that indicator
        years = set()

        # get all the data entries that use that indicator
        entries = main_models.Data.objects.filter(indicator=indicator)

        # get all the years from those entries
        for entry in entries:
            # get the period and add it to the years set
            years.add(entry.period[:4])

        # convert the set of years into a list
        years = list(years)

        # sort the years list from smallest to largest
        years = sorted(years)

        # convert all the years in the list back to strings
        for i in range(len(years)):
            years[i] = str(years[i])

        # reverse the sorted list so it goes from largest to smallest and remove duplicates
        years = reversed(years)

        # return the set of years
        return Response({"years": years}, 200)


class IndicatorValuetypeViewSet(CustomModelViewSet):
    serializer_class = api_routes_crud_serializers.IndicatorValuetypeSerializer
    queryset = main_models.IndicatorValuetype.objects.all()


class LinkViewSet(CustomModelViewSet):
    serializer_class = api_routes_crud_serializers.LinkSerializer
    queryset = main_models.Link.objects.all()


class DataViewSet(CustomModelViewSet):
    serializer_class = api_routes_crud_serializers.DataSerializer
    queryset = main_models.Data.objects.all().select_related()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        "location",
        "period",
        "datasource",
        "datasource__group",
        "indicator",
        "indicator__group",
        "value_type",
    ]

    @action(methods=["get"], detail=False)
    def indicator_set(self, request, *args, **kwargs):
        # get list of indicators from query parameter
        indicators: str = request.GET.get("indicators", None)
        indicators = indicators.strip()
        indicator_list = indicators.split(",")
        numerical_indicator_list = []

        for indicator in indicator_list:
            numerical_indicator_list.append(int(indicator))

        # check if indicators were passed as query parameters
        if not indicators:
            return Response({"detail": "indicator set was not specified"}, 400)

        # get data objects which have fall within the specified indicators
        print(numerical_indicator_list)
        data = main_models.Data.objects.filter(indicator__in=numerical_indicator_list)
        print(data)
        # serialize the queried data
        serializer = api_routes_crud_serializers.DataSerializer(data, many=True)

        # return the response of the serialized data
        return Response(serializer.data, 200)

    @swagger_auto_schema(
        method="post",
        serializer_class=api_routes_crud_serializers.DisaggregatedDataSerializer,
    )
    @swagger_auto_schema(
        method="get",
        serializer_class=api_routes_crud_serializers.DisaggregatedDataSerializer,
    )
    @action(
        methods=["get", "post"],
        detail=False,
        serializer_class=api_routes_crud_serializers.DisaggregatedDataSerializer,
    )
    def disaggregated(self, request, *args, **kwargs):
        """
        This is the endpoint for retrieving and creating disaggregation data
        """
        if request.method == "GET":
            disaggregated_data = main_models.DisaggregatedData.objects.all().select_related()

            serializer = api_routes_crud_serializers.DisaggregatedDataSerializer(
                disaggregated_data, many=True
            )

            return Response(serializer.data, 200)

        # if the request is a post request
        serializer = api_routes_crud_serializers.DisaggregatedDataSerializer(data=request.data)

        if not serializer.is_valid():
            # if the serializer is not valid return a 400 response
            return Response({"details": "Invalid input data entered"}, 400)

        serializer.save()

        return Response(serializer.data, 201)

    @action(methods=["get"], detail=False)
    def latest(self, request, *args, **kwargs):
        """
        This endpoint returns the date of the most recent data that was uploaded
        Args:
            request ([type]): [description]
        """
        latest_data = main_models.Data.objects.last()

        if not latest_data:
            return Response({"details": "No data was found"}, 400)

        date = latest_data.created_at
        return Response({"date": date}, 200)


class SubscriberViewSet(viewsets.ModelViewSet):
    serializer_class = api_routes_crud_serializers.SubscriberSerializer
    queryset = main_models.Subscriber.objects.all()


class DashboardViewSet(viewsets.ModelViewSet):
    serializer_class = api_routes_crud_serializers.DashboardSerializer
    queryset = main_models.Dashboard.objects.all()
