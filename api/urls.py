from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:companyRequested>/<str:stateRequested>/', views.getMenuForFrontEnd),
    path('randomOrder', views.getUserInput)
]
