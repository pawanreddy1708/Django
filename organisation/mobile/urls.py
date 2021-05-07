from django.urls import path,re_path
from . import views

urlpatterns = [
    path('',views.ProductCreateAPI().as_view(),name="ADD product"),
    path('<str:id>/',views.ProductOperationsAPI().as_view(),name="CRUD of products"),
    path('cart/<str:id>',views.AddToCartAPI().as_view(),name="Add products to CART"),
    re_path('search/(?P<item>.+)/$',views.SearchProductsAPI().as_view(),name="Search result"),
    re_path('search/sort/(?P<type>.+)/$',views.DisplayBySortedProducts().as_view(),name="Search sorted"),
    path('place-order/',views.PlaceOrderAPI().as_view(),name="Place order"),

]