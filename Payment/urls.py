from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import *


urlpatterns = [
    path("", views.paymentForm, name="payment"),
    path("success/", views.paymentSuccess, name="paiementSuccess"),
    path("cancel/", views.paymentCancel, name="paiementCancel"),
    # path("/", , name="")
    
]
