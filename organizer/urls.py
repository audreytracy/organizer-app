from django.urls import path
from organizer import views
from django.views.generic import RedirectView
from .views import CalendarView

urlpatterns = [
   path('', RedirectView.as_view(url='/login/', permanent=True)),
   path('weekly-calendar/', CalendarView.as_view(), name='weekly-calendar'),
   path('monthly-calendar/', CalendarView.as_view(), name='monthly-calendar'),
   path('monthly-calendar/<int:year>/<int:month>/', CalendarView.as_view(), name='monthly-calendar'),
   path('weekly_calendar/<int:acct_id>/', views.calendar, name='weekly_calendar'),
   path('monthly_calendar/<int:acct_id>/', views.monthly_calendar, name='monthly_calendar'),
   path('calendar/', views.calendar, name="calendar"),
   path('create/', views.create, name="create"),
   path('login/', views.login, name="login"),
]
