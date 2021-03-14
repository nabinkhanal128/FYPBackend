from django.urls import path, include
from rest_framework import routers, urls

from . import views as UserView

router = routers.DefaultRouter()
router.register('register', UserView.UserViewSet, basename='create user')
router.register('doctor', UserView.DoctorViewset, basename='doctor')
router.register('patient', UserView.PatientViewset, basename='patient')

urlpatterns = [
    path('', include(router.urls))
]