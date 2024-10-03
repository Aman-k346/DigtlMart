
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
    path("checkout", views.checkout, name="Checkout"),
    path("logout", views.logout_user, name="Logout"),
]
