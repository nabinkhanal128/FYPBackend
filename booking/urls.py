from django.urls import path, include
from rest_framework import routers, urls

from . import views as AppointmentBookView

router = routers.DefaultRouter()
router.register('appointment-book', AppointmentBookView.AppointmentBookViewset, basename='book-appointment')
router.register('insight', AppointmentBookView.InsightViewset, basename='appointment-insight')

urlpatterns = [
    path('', include(router.urls))
]