from django.urls import path
from . import views

urlpatterns = [
    path('',views.ProductCreateAPI().as_view(),name="ADD product"),
]