from django.urls import path
from . import views

urlpatterns = [
    path('ranking/<int:job_id>/', views.ranking, name='ranking'),
]
