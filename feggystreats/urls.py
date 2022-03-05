from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("cookies", views.cookies, name="cookies"),
    path("brownies", views.brownies, name="brownies"),
    path("checkout", views.checkout, name="checkout"),
    path("cart", views.cart, name="cart"),
    path("add_item/", views.addItem, name="add_item"),
    path("process_order/", views.processOrder, name="process_order"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)