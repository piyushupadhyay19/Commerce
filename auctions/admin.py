from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Listing, Category, Bid, Comment
from .forms import BidForm
# Register your models here.

# class ListingAdmin(admin.ModelAdmin):
#     readonly_fields = ('current_bid',)

class BidAdmin(admin.ModelAdmin):
    form = BidForm
    list_display = ('user', 'listing', 'bid')

    def save_model(self, request, obj, form, change):

        # Call the super method to perform the default save operation
        super().save_model(request, obj, form, change)

        # Update the current_bid of the associated listing
        listing = obj.listing
        if not listing.current_bid or obj.bid > listing.current_bid.bid:
            listing.current_bid = obj
            listing.save()

class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'current_bid', 'user',)
    search_fields = ['title']

    def get_current_bid_choices(self, current_listing_id):
        return Bid.objects.filter(listing_id=current_listing_id)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'current_bid':
            current_listing_id = request.resolver_match.kwargs.get('object_id')
            kwargs['queryset'] = self.get_current_bid_choices(current_listing_id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(User, UserAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Category)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment)