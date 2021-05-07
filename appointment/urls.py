from django.urls import path, include
from rest_framework import routers, urls

from . import views as AppointmentView

router = routers.DefaultRouter()
router.register('appointment', AppointmentView.AppointmentViewset, basename='appointment')
router.register('response', AppointmentView.ResponseViewset, basename='appointment-response')

urlpatterns = [
    path('', include(router.urls))
]