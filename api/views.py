from datetime import datetime, timedelta, time
from django.db.models import Sum, Max, Min, Avg, DateField
from django.db.models.functions import Trunc
from django.utils import timezone
from rest_framework import viewsets,status
from rest_framework.views import APIView, Response
from .models import Panel, OneHourElectricity
from .serializers import PanelSerializer, OneHourElectricitySerializer

class PanelViewSet(viewsets.ModelViewSet):
    queryset = Panel.objects.all()
    serializer_class = PanelSerializer

class HourAnalyticsView(APIView):
    serializer_class = OneHourElectricitySerializer
    def get(self, request, panelid):
        panelid = int(self.kwargs.get('panelid', 0))
        queryset = OneHourElectricity.objects.filter(panel_id=panelid)
        items = OneHourElectricitySerializer(queryset, many=True)
        return Response(items.data)
    def post(self, request, panelid):
        panelid = int(self.kwargs.get('panelid', 0))
        serializer = OneHourElectricitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DayAnalyticsView(APIView):
    def get(self, request, panelid):
        
        panelid = int(self.kwargs.get('panelid', 0))
        # Calculations end of the "yesterday" date/time
        today = datetime.now(tz=timezone.utc)
        yesterday = today - timedelta(days=1)
        time_last = time(23,59,59, tzinfo=timezone.utc)
        end_yesterday = datetime.combine(yesterday, time_last)
        # Forming DateSet according required conditions.
        # Project Task is defined as:
        # Get data [sum, min, max, average of hourly kilowatt values] 
        # for current panel by each day 
        # up to the end of the previous day.
        report_kwatts = OneHourElectricity.objects \
            .filter(panel__exact=panelid) \
            .filter(date_time_db__lte=end_yesterday) \
            .annotate(date_time=Trunc('date_time_db', 'day', output_field=DateField())) \
            .values('date_time') \
            .annotate(sum=Sum('kilo_watt')) \
            .annotate(average=Avg('kilo_watt')) \
            .annotate(maximum=Max('kilo_watt')) \
            .annotate(minimum=Min('kilo_watt'))
        
        return Response(report_kwatts)
        
'''        return Response([{
            "date_time": "[date for the day]",
            "sum": 0,
            "average": 0,
            "maximum": 0,
            "minimum": 0
        }])
'''