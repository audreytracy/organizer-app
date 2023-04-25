from django.shortcuts import redirect, render
from organizer.models import Account, Category, Event
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.views.generic import TemplateView
from django.utils import timezone
from calendar import monthrange
from datetime import timedelta

# id of the current logged in user (to make passing data btwn views easier)
logged_in_user:int = 0

def login(request):
    '''
    log in
    '''
    if request.method == 'POST':
        username = str(request.POST.get('username_text_box'))
        email = request.POST.get('email_text_box')
        password = request.POST.get('pwd_text_box')
        if not username or not email or not password:
            return render(request, "organizer/login.html", context={'user_not_found_message': "missing fields"})
        if not Account.objects.filter(username = username, password = password, email = email).exists():
            return render(request, "organizer/login.html", context={'user_not_found_message': "user not found"})
        global logged_in_user
        logged_in_user =  Account.objects.filter(username = username, password = password, email = email).first().pk
        return redirect('calendar')
    return render(request, "organizer/login.html", context=None)
    

def create(request):
    '''
    create account
    '''
    if request.method == 'POST':
        username = str(request.POST.get('username_text_box'))
        email = request.POST.get('email_text_box')
        password = request.POST.get('pwd_text_box')
        if not username or not email or not password:
            return render(request, "organizer/create.html", context={'success_message': "missing fields"})
        Account.objects.create(username = username, email = email, password = password)
        return render(request, 'organizer/create.html', context = {'success_message' : "account created successfully!"})
    return render(request, 'organizer/create.html', context = None)

def settings(request):
    global logged_in_user
    if logged_in_user == 0:
        return render(request, "organizer/login.html", context=None)
    if request.method == 'POST':
        user = Account.objects.get(pk = logged_in_user)
        username = request.POST.get('username_text_box')
        email = request.POST.get('email_text_box')
        category_name = request.POST.get('myCategories')
        password = request.POST.get('password_text_box')
        color = request.POST.get('colors')
        if category_name and color:
            Category.objects.update_or_create(name = category_name, account_id_id = user.account_id, defaults ={'color':color})
            messages.info(request, "category info saved!")
        if username and username != user.username:
            Account.objects.update_or_create(account_id = user.account_id, defaults ={'username':username})
            messages.info(request, "updated username")
        if password and password != user.password:
            Account.objects.update_or_create(account_id = user.account_id, defaults ={'password':password})
            messages.info(request, "updated password")
        if email and email != user.email:
            Account.objects.update_or_create(account_id = user.account_id, defaults ={'email':email})
            messages.info(request, "updated email")
    data = Account.objects.values('email','password', 'created_on', 'category__name', 'category__color').filter(account_id = logged_in_user).distinct()
    return render(request, "organizer/settings.html", context={'data':data})

def calendar(request):
    global logged_in_user
    if logged_in_user == 0:
        return render(request, "organizer/login.html", context=None)
    return render(request, "organizer/calendar.html", context={'acct_id' : logged_in_user})

def logout(request):
    global logged_in_user
    logged_in_user = 0
    return render(request, "organizer/login.html", context={'user_not_found_message': "successfully logged out"})

def events(request):
    global logged_in_user
    if logged_in_user == 0:
        return render(request, "organizer/login.html", context=None)
    events = Event.objects.filter(account_id = logged_in_user).order_by("event_start_date")
    categories = Category.objects.filter(account_id = logged_in_user).order_by("name")
    return render(request, "organizer/events.html", context={'events': events, 'acct' : logged_in_user, 'categories': categories})

def command(request, id, cmd):
    event = Event.objects.get(pk = id)
    acct = logged_in_user
    if cmd == "delete":
        event.delete()
    if cmd == "details":
        return render(request, "organizer/event_detail.html", context={'event' : event})
    #return render(request, "organizer/events.html", context={'events' : Event.objects.filter(account_id = acct).order_by("event_start_date")})
    return redirect('events')


class WeeklyCalendarView(TemplateView):
    template_name = 'organizer/calendar.html'


    def get_context_data(self, month = None, year = None, **kwargs):
        context = super().get_context_data(**kwargs)
        year = int(self.request.GET.get('year', timezone.now().year))
        month = int(self.request.GET.get('month', timezone.now().month))

        # Calculate the first and last days of the week
        # (Assuming Sunday is the first day of the week)
        first_day_of_month = timezone.datetime(year, month, 1)
        weekdays_lookup = {'Sunday':0,'Monday':1,'Tuesday':2,'Wednesday':3,'Thursday':4,'Friday':5,'Saturday':6}
        first_day_shift = weekdays_lookup[first_day_of_month.strftime('%A')] # how many days you need to skip to 
        last_day_of_month = timezone.datetime(year, month, monthrange(year, month)[1])
        first_day_of_week = first_day_of_month - timedelta(days=first_day_of_month.weekday())
        while first_day_of_week.month != month: # adjust if first day of week is not in the same month
            first_day_of_week = first_day_of_week + timedelta(days=1)

        # Generate a list of dates representing each day of the week
        dates = ['' for i in range(first_day_shift)]
        for i in range(last_day_of_month.day):
            date = first_day_of_week + timedelta(days=i)
            dates.append(date)
        months = {1:'January', 2:'February', 3:'March', 4:'April',5:'May', 6:'June', 7:'July', 8:'August',9:'September', 10:'October', 11:'November', 12:'December'}
        # Add the year, month, first_day_of_week, and last_day_of_week to the context
        context['year'] = year
        context['month'] = months[month]
        context['month_num'] = month
        context['dates'] = dates
        return context

def addEvent(request):
    acct_id = logged_in_user
    cats = Category.objects.filter(account_id = acct_id).order_by("name")
    if request.method == 'POST':
        acct = Account.objects.get(pk=acct_id)
        category_id = request.POST.get('category_box')
        location = request.POST.get('location_text_box')
        event_start_date = request.POST.get('sdate')
        event_start_time = request.POST.get('stime')
        event_end_date = request.POST.get('edate')
        event_end_time = request.POST.get('etime')
        name = request.POST.get('n')
        description = request.POST.get('description')
        if not location or not event_start_date or not name or not description:
            return render(request, "organizer/add_event.html", context={'acct' : acct_id,'success_message': "missing fields", 'cats': cats})
        elif not event_start_time and not event_end_time and not event_end_date:
            Event.objects.create(account_id = acct, category_id = category_id, location = location, name = name, description = description, event_start_date = event_start_date)
        elif not event_start_time and not event_end_time:
            Event.objects.create(event_end_date = event_end_date, account_id = acct, category_id = category_id, location = location, name = name, description = description, event_start_date = event_start_date)
        elif not event_start_time and not event_end_date:
            Event.objects.create(event_event_end_time = event_end_time, account_id = acct, category_id = category_id, location = location, name = name, description = description, event_start_date = event_start_date)
        elif not event_end_time and not event_end_date:
            Event.objects.create(event_start_time = event_start_time, account_id = acct, category_id = category_id, location = location, name = name, description = description, event_start_date = event_start_date)
        elif not event_start_time:
            Event.objects.create(account_id = acct, category_id = category_id, location = location, event_start_date = event_start_date, event_end_date = event_end_date, event_end_time = event_end_time, name = name, description = description)
        elif not event_end_time:
            Event.objects.create(account_id = acct, category_id = category_id, location = location, event_start_date = event_start_date, event_start_time = event_start_time, event_end_date = event_end_date, name = name, description = description)
        elif not event_end_date:
            Event.objects.create(account_id = acct, category_id = category_id, location = location, event_start_date = event_start_date, event_start_time = event_start_time, event_end_time = event_end_time, name = name, description = description)
        else:
            Event.objects.create(account_id = acct, category_id = category_id, location = location, event_start_date = event_start_date, event_start_time = event_start_time, event_end_date = event_end_date, event_end_time = event_end_time, name = name, description = description)
        return render(request, 'organizer/add_event.html', context = {'acct' : acct_id,'success_message' : "account created successfully!", 'cats': cats})
    return render(request, 'organizer/add_event.html', context = {'acct' : acct_id, 'cats': cats})