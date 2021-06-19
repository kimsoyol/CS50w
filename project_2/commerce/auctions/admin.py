from django.contrib import admin

from .models import Listing, User, WatchList, Comment, Bid, Category

class ItemAdmin(admin.ModelAdmin):
    list_display = ('id','item', 'price', 'author', 'active', 'categories')

class WatchedItemAdmin(admin.ModelAdmin):
    list_display = ('item','author')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'text', 'author')

class BidAdmin(admin.ModelAdmin):
    list_display = ('item', 'amount', 'author')


admin.site.register(Listing, ItemAdmin)
admin.site.register(User)
admin.site.register(WatchList, WatchedItemAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Category)



