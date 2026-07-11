from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    home, create_event, edit_event, event_detail, join_event, cancel_seat, 
    my_bookings, my_events, register_view, login_view, logout_view
)

urlpatterns = [
    path('', home, name="home"),
    path('create_event/', create_event, name="create_event"),
    path('event/<int:event_id>/edit/', edit_event, name="edit_event"),  # ADDED: URL pattern for editing
    path('event/<int:event_id>/', event_detail, name='event_detail'),
    path('event/<int:event_id>/join/', join_event, name='join_event'),
    path('event/<int:event_id>/cancel/', cancel_seat, name='cancel_seat'),
    path('my/bookings/', my_bookings, name='my_bookings'),
    path('my/events/', my_events, name='my_events'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    
    # Password Reset Routes
    path(
        'password-reset/', 
        auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), 
        name='password_reset'
    ),
    path(
        'password-reset/done/', 
        auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), 
        name='password_reset_done'
    ),
    path(
        'password-reset-confirm/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), 
        name='password_reset_confirm'
    ),
    path(
        'password-reset-complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), 
        name='password_reset_complete'
    ),
]