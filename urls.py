from django.urls import path
from . import views

urlpatterns = [
    # Home & Auth
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Houses
    path('houses/', views.house_list, name='house_list'),
    path('houses/<int:pk>/', views.house_detail, name='house_detail'),
    path('houses/create/', views.create_house, name='create_house'),
    path('houses/<int:pk>/update/', views.house_update, name='house_update'),
    path('houses/<int:pk>/delete/', views.house_delete, name='house_delete'),
    path('book/<int:house_id>/', views.book_house, name='book_house'),
    path('unbook/<int:house_id>/', views.unbook_house, name='unbook_house'),

    # Landlords
    path('landlords/', views.landlord_list, name='landlord_list'),
    path('landlords/<int:pk>/', views.landlord_detail, name='landlord_detail'),
    path('landlord/dashboard/', views.landlord_dashboard, name='landlord_dashboard'),

    # Riders
    path('riders/', views.rider_list, name='rider_list'),
    path('riders/<int:pk>/', views.rider_detail, name='rider_detail'),
    path('rider/workspace/', views.rider_workspace, name='rider_workspace'),

    # Bookings
    path('bookings/', views.booking_list, name='booking_list'),
    path('bookings/<int:pk>/', views.booking_detail, name='booking_detail'),

    # SMS Logs
    path('smslogs/', views.smslog_list, name='smslog_list'),
    path('smslogs/<int:pk>/', views.smslog_detail, name='smslog_detail'),

    # Custom dashboards
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/admin/manage-users/', views.manage_users, name='manage_users'),
    path('dashboard/admin/edit-user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('dashboard/admin/delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('dashboard/admin/export-users/', views.export_users_excel, name='export_users_excel'),
    path('dashboard/ceo/', views.ceo_dashboard, name='ceo_dashboard'),
    path('dashboard/manager/', views.manager_dashboard, name='manager_dashboard'),
]