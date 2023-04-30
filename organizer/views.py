from django.shortcuts import render
from organizer.models import Account

from django.views.generic import TemplateView
from django.utils import timezone
from calendar import monthrange
from datetime import timedelta
from datetime import date

class CalendarView(TemplateView):
    template_name = 'weekly_calendar.html'

    def get_template_names(self):
        if 'week' in self.request.GET:
            return ['weekly_calendar.html']
        elif 'month' in self.request.GET:
            return ['monthly_calendar.html']
        else:
            return super().get_template_names()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the year and month from the URL parameters or the current date
        year = int(self.request.GET.get('year', timezone.now().year))
        month = int(self.request.GET.get('month', timezone.now().month))

        # Calculate the first and last days of the month
        first_day_of_month = date(year, month, 1)
        last_day_of_month = date(year, month, monthrange(year, month)[1])

        # Generate a list of dates representing each day of the month
        dates = []
        for day in range(1, last_day_of_month.day + 1):
            date_obj = date(year, month, day)
            dates.append(date_obj)

        # Generate a list of weeks, where each week is a list of 7 days
        weeks = []
        week = []
        for i, day in enumerate(dates):
            week.append(day)
            if (i + 1) % 7 == 0:
                weeks.append(week)
                week = []

        # Calculate the previous and next month dates for the links
        prev_month = month - 1 if month > 1 else 12
        prev_year = year - 1 if month == 1 else year
        next_month = month + 1 if month < 12 else 1
        next_year = year + 1 if month == 12 else year

        # Add the year, month, month_name, dates, and link dates to the context
        context['year'] = year
        context['month'] = month
        context['month_name'] = timezone.datetime(year, month, 1).strftime('%B')
        context['dates'] = dates
        context['prev_year'] = prev_year
        context['prev_month'] = prev_month
        context['next_year'] = next_year
        context['next_month'] = next_month

        return context

    # def get_events_for_day(self, day):
    #     # Get the events for the given day
    #     events = Event.objects.filter(date=day)

    #     return events

def monthly_calendar(request, acct_id):
    return render(request, "organizer/monthly_calendar.html", context={'acct_id' : acct_id})

def weekly_calendar(request, acct_id):
    return render(request, "organizer/weekly_calendar.html", context={'acct_id' : acct_id})

def calendar(request, acct_id):
    return render(request, "organizer/weekly_calendar.html", context={'acct_id' : acct_id})

def login(request):
    if request.method == 'POST':
        username = str(request.POST.get('username_text_box'))
        email = request.POST.get('email_text_box')
        password = request.POST.get('pwd_text_box')
        if not username or not email or not password:
            return render(request, "organizer/login.html", context={'user_not_found_message': "missing fields"})
        if not Account.objects.filter(username = username, password = password, email = email).exists():
            return render(request, "organizer/login.html", context={'user_not_found_message': "user not found"})
        acct_id =  Account.objects.filter(username = username, password = password, email = email).first().pk
        return calendar(request, acct_id)
    return render(request, "organizer/login.html", context=None)
    
def create(request):
    if request.method == 'POST':
        username = str(request.POST.get('username_text_box'))
        email = request.POST.get('email_text_box')
        password = request.POST.get('pwd_text_box')
        if not username or not email or not password:
            return render(request, "organizer/create.html", context={'success_message': "missing fields"})
        Account.objects.create(username = username, email = email, password = password)
        return render(request, 'organizer/create.html', context = {'success_message' : "account created successfully!"})
    return render(request, 'organizer/create.html', context = None)
