from django.shortcuts import render
from organizer.models import Account

from django.views.generic import TemplateView
from django.utils import timezone
from calendar import monthrange
from datetime import timedelta

class WeeklyCalendarView(TemplateView):
    template_name = 'weekly_calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the year and month from the URL parameters or the current date
        year = int(self.request.GET.get('year', timezone.now().year))
        month = int(self.request.GET.get('month', timezone.now().month))

        # Calculate the first and last days of the week
        # (Assuming Sunday is the first day of the week)
        first_day_of_month = timezone.datetime(year, month, 1)
        last_day_of_month = timezone.datetime(year, month, monthrange(year, month)[1])
        first_day_of_week = first_day_of_month - timedelta(days=first_day_of_month.weekday())
        last_day_of_week = last_day_of_month + timedelta(days=6 - last_day_of_month.weekday())

        # Generate a list of dates representing each day of the week
        dates = []
        for i in range(7):
            date = first_day_of_week + timedelta(days=i)
            dates.append(date)

        # Add the year, month, first_day_of_week, and last_day_of_week to the context
        context['year'] = year
        context['month'] = month
        context['first_day_of_week'] = first_day_of_week
        context['last_day_of_week'] = last_day_of_week
        context['dates'] = dates
        
        return context



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

def calendar(request, acct_id):
    return render(request, "organizer/weekly_calendar.html", context={'acct_id' : acct_id})