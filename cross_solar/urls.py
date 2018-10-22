from django.urls import path, include
from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router.register('panel', views.PanelViewSet)

urlpatterns = [
    path('panel/', include('api.urls')),
]

urlpatterns += router.urls
