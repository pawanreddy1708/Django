from django.urls import path
from . import views


urlpatterns = [
    path('', views.all_api,name="API's"),
    path('find-all/',views.findAll,name="All Employees"),
    path('find-one/<str:pk>',views.findOne,name="Employee"),
    path('create-employee/',views.createOne,name="Create employee"),
    path('update-one/<str:pk>',views.updateOrDeleteOne,name="Update Employee"),
    path('delete-one/<str:pk>',views.updateOrDeleteOne,name="Delete employee")
]