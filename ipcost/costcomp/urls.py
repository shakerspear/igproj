from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("<int:counsoler_id>", views.counsoler, name='counsoler'),
]
