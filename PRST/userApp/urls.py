from userApp import views
from django.urls import path

urlpatterns = [
    path('login/', views.home, name="login"),
    path('login/<slug:kind>', views.login, name="login"),
    path('register/<slug:kind>', views.register, name="register"),
]