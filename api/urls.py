from django.urls import path
from . import views
	
# Refactoring by Project Task
app_name = 'api'
urlpatterns = [
    path('<int:panelid>/analytics/', views.HourAnalyticsView.as_view(), name='HourAnalyticsView'),
    path('<int:panelid>/analytics/day/', views.DayAnalyticsView.as_view(), name='DayAnalyticsView'),
]
