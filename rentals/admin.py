from django.contrib import admin
from .models import House, Landlord, Rider

class HouseAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'is_booked', 'landlord')

admin.site.register(House, HouseAdmin)
admin.site.register(Landlord)
admin.site.register(Rider)