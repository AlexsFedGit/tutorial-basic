from django.urls import path

from advertisement import views

urlpatterns = [
    path('', views.advertisement_list, name='advertisement_list'),
]