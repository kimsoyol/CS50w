from django.urls import path

from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("category/", views.category, name="category"),
    path("category/<int:category_id>", views.categoryItems, name="categoryItems"),
    path("listings/<int:item_id>", views.item, name="item"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("create/", views.Create.as_view(), name="create"),
    path("listings/<int:item_id>/remove", views.removeWatchList, name="removeWatchList"),
    path("listings/<int:item_id>/comment", views.comment, name="comment"),
    path("listings/<int:item_id>/bid", views.bid, name="bid"),
    path("listings/<int:item_id>/deactive", views.removeListing, name="removeListing"),

    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
