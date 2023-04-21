from django.shortcuts import render, redirect
from organizer.models import Account, Event, Category


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
        return events(request, acct_id)
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
    return render(request, "organizer/calendar.html", context={'acct_id' : acct_id})

def events(request, acct):
    events = Event.objects.filter(account_id = acct).order_by("event_start_date")
    categories = Category.objects.filter(account_id = acct).order_by("name")
    return render(request, "organizer/events.html", context={'events': events, 'acct' : acct, 'categories': categories})

def command(request, id, cmd):
    event = Event.objects.get(pk = id)
    acct = event.account_id
    if cmd == "delete":
        event.delete()
    if cmd == "details":
        return render(request, "organizer/event_detail.html", context={'event' : event})
    #return render(request, "organizer/events.html", context={'events' : Event.objects.filter(account_id = acct).order_by("event_start_date")})
    return redirect('events', acct=acct.account_id)