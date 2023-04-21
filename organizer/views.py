from django.shortcuts import render
from organizer.models import Account, Category
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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
        return calendar(request)
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

@login_required(login_url="login")
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
    if logged_in_user == 0:
        return render(request, "organizer/login.html", context=None)
    return render(request, "organizer/calendar.html", context={'acct_id' : logged_in_user})

def logout(request):
    global logged_in_user
    logged_in_user = 0
    return render(request, "organizer/login.html", context={'user_not_found_message': "successfully logged out"})