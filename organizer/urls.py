from django.urls import path
from organizer import views
from django.views.generic import RedirectView

from .views import WeeklyCalendarView

urlpatterns = [
   path('', RedirectView.as_view(url='/login/', permanent=True)),
   path('weekly-calendar/', WeeklyCalendarView.as_view(), name='weekly-calendar'),

   path('calendar/', views.calendar, name="calendar"),
   path('create/', views.create, name="create"),
   path('login/', views.login, name="login"),
]