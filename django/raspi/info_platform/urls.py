from django.urls import path
from . import views

urlpatterns=[
    path('show_pi_info/',views.show_pi_info, name='info')
]