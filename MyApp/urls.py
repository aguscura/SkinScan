from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework import routers

router.register("MyApp", views.operacionViews)

urlpatterns = [
    path('', views.cxcontact , name= "Subir imagen"),
    path('api/', include(router.urls)),

]