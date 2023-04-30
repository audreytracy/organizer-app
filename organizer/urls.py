from django.urls import path
from organizer import views
from django.views.generic import RedirectView


urlpatterns = [
    path('', RedirectView.as_view(url='/login/', permanent=True)),
    path('calendar/', views.WeeklyCalendarView.as_view(), name='calendar'),
    path('calendar/<int:year>/<int:month>/', views.WeeklyCalendarView.as_view(), name='calendar2'),
    path('create/', views.create, name="create"),
    path('login/', views.login, name="login"),
    path('settings/', views.settings, name="settings"),
    path('logout/', views.logout, name="logout"),
    path('events/', views.events, name="events"),
    path('command/<int:id>/<str:cmd>', views.command, name = "command"),
    path('add_event/', views.addEvent, name="addevent"),
    path('to_do/', views.to_do, name="to_do"),
    path('add_task/', views.add_task, name="add_task"),
    path('edit_task/<int:id>/', views.edit_task, name = "edit_task"),
    path('delete_task/<int:id>/', views.delete_task, name = "delete_task"),
    path('complete_task/<int:id>/', views.complete_task, name = "complete_task"),
]