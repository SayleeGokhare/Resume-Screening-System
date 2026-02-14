from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('applications/', views.my_applications, name='my_applications'),
]
