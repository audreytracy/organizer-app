from django.urls import path
from organizer import views
from django.views.generic import RedirectView


urlpatterns = [
   path('', RedirectView.as_view(url='/login/', permanent=True)),
   path('calendar/', views.calendar, name="calendar"),
   path('create/', views.create, name="create"),
   path('login/', views.login, name="login"),
   path('settings/', views.settings, name="settings"),
   path('logout/', views.logout, name="logout"),
   path('events/', views.events, name="events"),
   path('command/<id>/<cmd>', views.command),
]