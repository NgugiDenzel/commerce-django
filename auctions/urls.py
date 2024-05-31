from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("auction", views.auction_listing, name="auction"),
    path("listings/<str:Title>", views.listing_page, name="listings"),
    path("category", views.category, name="category"),
    path("category/<str:category>", views.category_list, name="category_list"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("watchlist/add/<str:Title>",
         views.add_to_watchlist, name="add_watchlist"),
    # path("listings/<str:Title>/bid", views.place_bid, name="place_bid"),
    path("watchlist/remove/<str:Title>",
         views.remove_from_watchlist, name="remove_watchlist")


]
# urls.py


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
