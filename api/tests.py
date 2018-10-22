from rest_framework.test import APITestCase
from rest_framework import status
from datetime import datetime
from django.utils import timezone
from .models import Panel, OneHourElectricity

class PanelTestCase(APITestCase):
    def setUp(self):
        Panel.objects.create(brand="Areva", serial="AAAA1111BBBB2222", latitude=12.345678, longitude=178.765543)
        OneHourElectricity.objects.create(panel_id=1, kilo_watt=100, date_time=datetime.now(tz=timezone.utc))
        OneHourElectricity.objects.create(panel_id=1, kilo_watt=150, date_time="2018-09-01 01:00:00+00:00")
        OneHourElectricity.objects.create(panel_id=1, kilo_watt=200, date_time="2018-09-01 02:00:00+00:00")

    def test_panel_listing(self):
        response = self.client.get('/panel/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_panel_get(self):
        response = self.client.get('/panel/1/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["serial"], "AAAA1111BBBB2222")

    def test_day_analytics_listing(self):
        response = self.client.get('/panel/1/analytics/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_day_analytics_get(self):
        response = self.client.get('/panel/1/analytics/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_day_analytics_day_get(self):
        response = self.client.get('/panel/1/analytics/day/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
