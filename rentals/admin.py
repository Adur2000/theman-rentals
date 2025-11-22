from django.contrib import admin
from django.utils.html import format_html
from .models import House, Landlord, Rider

class HouseAdmin(admin.ModelAdmin):
    list_display = ('colored_title', 'location', 'colored_status', 'landlord')
    list_filter = ('is_booked', 'location')
    search_fields = ('title', 'location', 'landlord__user__username')

    def colored_title(self, obj):
        return format_html('<span style="color:#3498db; font-weight:bold;">{}</span>', obj.title)
    colored_title.short_description = "House Title"

    def colored_status(self, obj):
        if obj.is_booked:
            return format_html('<span style="color:green; font-weight:bold;">Booked ✅</span>')
        return format_html('<span style="color:red; font-weight:bold;">Available 🏠</span>')
    colored_status.short_description = "Status"

class LandlordAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'colored_area')

    def colored_area(self, obj):
        return format_html('<span style="color:#8e44ad;">{}</span>', obj.area)
    colored_area.short_description = "Area"

class RiderAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'colored_price', 'area')

    def colored_price(self, obj):
        return format_html('<span style="color:#e67e22; font-weight:bold;">KES {}</span>', obj.price)
    colored_price.short_description = "Delivery Price"

# Register models with custom admin
admin.site.register(House, HouseAdmin)
admin.site.register(Landlord, LandlordAdmin)
admin.site.register(Rider, RiderAdmin)

# Customize admin site headers
admin.site.site_header = "🏠 The Man Rentals Admin"
admin.site.site_title = "The Man Rentals Dashboard"
admin.site.index_title = "Welcome to The Man Rentals Administration"