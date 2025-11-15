
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from rentals import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('rentals.urls')),  # include your app routes
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),  # optional
    path('admin/manage-users/', views.manage_users, name='manage_users'),
]
