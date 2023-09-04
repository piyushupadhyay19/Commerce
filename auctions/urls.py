from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("mylistings", views.mylisting, name="mylistings"),
    path("create", views.create, name="create"),
    path("categories", views.categories, name="categories"),
    path("category/<str:category>", views.categorylisting, name="category"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("removelisting/<int:listing_id>", views.removelisting, name="removelisting"),
]
