from django.urls import path
from . import views

urlpatterns = [
    path('productionplan/', views.production_plan),
]
