from django.contrib import admin

from .models import Listing, User, WatchList


admin.site.register(Listing)
admin.site.register(User)
admin.site.register(WatchList)
