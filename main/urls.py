
from django.urls import path

from . import views





urlpatterns = [
    path("", views.home, name="home"),
    path("terms", views.terms, name="terms"),
    path("bundle/video", views.VideoBundle, name="VideoBundle"),
    path("refund", views.refund, name="Refund"),
    path("privacy", views.privacy, name="Privacy"),
    path("login", views.login, name="Login"),
    path("register", views.register, name="Register"),
    path("logout", views.logout_user, name="Logout"),

    # Payment
    path("checkout", views.checkout, name="checkout"),
    path('payment-initiate', views.initiate_payment, name='initiate_payment'),
    path('callback', views.payment_callback, name='callback'),
    path('success', views.success_page, name='success'),
    path('failed', views.failed_page, name='failed'),


]
