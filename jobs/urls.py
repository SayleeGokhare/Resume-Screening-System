from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('create/', views.create_job, name='create_job'),
    path('apply/<int:job_id>/', views.apply_job, name='apply_job'),
]
