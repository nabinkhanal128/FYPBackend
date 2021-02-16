from django.urls import path, include
from rest_framework import routers, urls

from . import views as UserView

router = routers.DefaultRouter()
router.register('user-create', UserView.UserViewSet, basename='create user')
router.register('patient', UserView.PatientViewset, basename='patient')
router.register('doctor', UserView.DoctorViewset, basename='doctor')


urlpatterns = [
    path('', include(router.urls))
]