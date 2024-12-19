from django.urls import path
from . import views

urlpatterns = [
    path('<str:ticker>/', views.options_view, name='options_view'),
    path('evaluate/', views.option_detail_view, name='option_detail_view'),
]