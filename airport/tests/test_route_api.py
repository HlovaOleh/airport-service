from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from rest_framework.test import APIClient

from airport.models import Route, Airport
from airport.serializers import RouteListSerializer

ROUTE_URL = reverse("airport:route-list")


def sample_airport(**params):
    defaults = {
        "name": "testairport",
        "closest_big_city": "testcity",
    }
    defaults.update(params)

    return Airport.objects.create(**defaults)


def sample_route(**params):
    source = sample_airport(name="testtairport", closest_big_city="testtcity")
    destination = sample_airport(name="testttairport", closest_big_city="testttcity")
    defaults = {
        "source": source,
        "destination": destination,
        "distance": 500,
    }
    defaults.update(params)

    return Route.objects.create(**defaults)


class UnauthenticatedRouteAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        response = self.client.get(ROUTE_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedRouteAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@testmail.com",
            "testtset",
        )
        self.client.force_authenticate(self.user)

    def test_list_routes(self):
        airport_start = sample_airport(name="testairport2")
        airport_end = sample_airport(name="testairport1")
        sample_route(source=airport_start, destination=airport_end)

        routes = Route.objects.all()
        serializer = RouteListSerializer(routes, many=True)

        response = self.client.get(ROUTE_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_filter_routes_by_airports_name(self):
        airport_start = sample_airport(name="testairport2")
        airport_end = sample_airport(name="testairport1")
        route_1 = sample_route(source=airport_start, destination=airport_end)
        route_2 = Route.objects.create(source=airport_end, destination=airport_start, distance=690)

        serializer_1 = RouteListSerializer(route_1)
        serializer_2 = RouteListSerializer(route_2)

        response = self.client.get(ROUTE_URL, {"source": airport_start.name})

        self.assertIn(serializer_1.data, response.data)
        self.assertNotIn(serializer_2.data, response.data)

        response = self.client.get(ROUTE_URL, {"destination": airport_end.name})

        self.assertIn(serializer_1.data, response.data)
        self.assertNotIn(serializer_2.data, response.data)

    def test_create_route_forbidden(self):
        airport_start = sample_airport(name="testtairport")
        airport_end = sample_airport(name="testttairport")
        payload = {
            "source": airport_start,
            "destination": airport_end,
            "distance": 690,
        }

        response = self.client.post(ROUTE_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminRouteAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@testmail.com", "testtset", is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_route(self):
        airport_start = sample_airport(name="testtairport")
        airport_end = sample_airport(name="testttairport")
        payload = {
            "source": airport_start.id,
            "destination": airport_end.id,
            "distance": 690,
        }

        response = self.client.post(ROUTE_URL, payload)
        route = Route.objects.get(id=response.data["id"])

        source = route.source
        del payload["source"]

        destination = route.destination
        del payload["destination"]

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        for key in payload:
            self.assertEqual(payload[key], getattr(route, key))

        self.assertEqual(airport_start, source)
        self.assertEqual(airport_end, destination)
