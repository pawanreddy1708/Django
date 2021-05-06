from django.urls import path
from . import views
urlpatterns = [
    path('register/',views.register().as_view(),name="Register"),
    path('verify-otp/',views.verifyOTP().as_view(),name="Verify OTP"),
    path('login/',views.LoginAPI().as_view(),name="Login"),
    path('logout/',views.LogoutAPI().as_view(),name="Logout")
]