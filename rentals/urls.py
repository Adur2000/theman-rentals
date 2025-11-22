from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    # Public routes
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('houses/', views.house_list, name='house_list'),
    path('book/<int:house_id>/', views.book_house, name='book_house'),
    path('unbook/<int:house_id>/', views.unbook_house, name='unbook_house'),

    # Rider routes
    path('rider/workspace/', views.rider_workspace, name='rider_workspace'),

    # Landlord routes
    path('landlord/dashboard/', views.landlord_dashboard, name='landlord_dashboard'),

    # Custom admin dashboard (your own views, not Django admin)
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/admin/manage-users/', views.manage_users, name='manage_users'),
    path('dashboard/admin/edit-user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('dashboard/admin/delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('dashboard/admin/export-users/', views.export_users_excel, name='export_users_excel'),
    path('dashboard/ceo/', views.ceo_dashboard, name='ceo_dashboard'),
    path('dashboard/manager/', views.manager_dashboard, name='manager_dashboard'),


    # House management
    path('create-house/', views.create_house, name='create_house'),

    # Django’s built-in admin site
    path('admin/', admin.site.urls),

    # Django’s built-in auth (login/logout/password reset)
    path('accounts/', include('django.contrib.auth.urls')),

]



