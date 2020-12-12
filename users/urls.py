from django.urls import path, include
from . import views as UserView
from rest_framework import routers, urls

router = routers.DefaultRouter()
router.register('user-create', UserView.RegisterView)


urlpatterns =[
    path('', include(router.urls)) 
]