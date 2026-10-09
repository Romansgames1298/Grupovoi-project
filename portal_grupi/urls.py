from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import (dashboard_view, event_create, event_delete, event_edit, events_view,
                     forum_view, home, login_view, profile_view, register_view,
                     topic_create, topic_delete, topic_edit, topic_view)

urlpatterns = [
    path('', home, name='home'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('profile/', profile_view, name='profile'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('forum/', forum_view, name='forum'),
    path('forum/topic/<int:topic_id>/', topic_view, name='topic'),
    path('forum/topic/new/', topic_create, name='topic_create'),
    path('forum/topic/<int:topic_id>/edit/', topic_edit, name='topic_edit'),
    path('forum/topic/<int:topic_id>/delete/', topic_delete, name='topic_delete'),
    path('events/', events_view, name='events'),
    path('events/new/', event_create, name='event_create'),
    path('events/<int:event_id>/edit/', event_edit, name='event_edit'),
    path('events/<int:event_id>/delete/', event_delete, name='event_delete'),
]
