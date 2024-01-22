from django.shortcuts import render
from rest_framework import mixins, viewsets

from airport.models import (
    Airport,
    Airplane,
    AirplaneType,
    Crew,
    Route,
    Order,
    Flight
)
from airport.permissions import IsAuthenticatedOrIsAdminReadOnly
from airport.serializers import (
    AirportSerializer,
    AirplaneSerializer,
    AirplaneTypeSerializer,
    CrewSerializer,
    RouteSerializer,
    OrderSerializer,
    FlightSerializer
)


class AirportViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    permission_classes = (IsAuthenticatedOrIsAdminReadOnly,)


class RouteViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = (IsAuthenticatedOrIsAdminReadOnly,)


class AirplaneTypeViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer
    permission_classes = (IsAuthenticatedOrIsAdminReadOnly,)


class AirplaneViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer
    permission_classes = (IsAuthenticatedOrIsAdminReadOnly,)


class CrewViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
    permission_classes = (IsAuthenticatedOrIsAdminReadOnly,)


class OrderViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticatedOrIsAdminReadOnly,)


class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes = (IsAuthenticatedOrIsAdminReadOnly,)
