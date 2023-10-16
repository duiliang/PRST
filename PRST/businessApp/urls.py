from django.urls import path
from businessApp.views import *

urlpatterns = [
    path('<slug:kind>/', home, name="business"),
]
