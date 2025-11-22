from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Django’s built-in admin site
    path('admin/', admin.site.urls),

    # Include all routes from the rentals app
    path('', include('rentals.urls')),

    # Django’s built-in auth (login/logout/password reset)
    path('accounts/', include('django.contrib.auth.urls')),
]
