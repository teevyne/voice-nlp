from django.urls import path
from .views import execution_method

urlpatterns = [
    path('analyse/', execution_method, name='analyse'),
]
