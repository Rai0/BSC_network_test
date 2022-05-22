from django.urls import path, include
from .views import *

urlpatterns = [
    path ('', tx_page),
    path ('make_tx', make_tx),
    path('tx/<str:tx>', tx_description),
]
