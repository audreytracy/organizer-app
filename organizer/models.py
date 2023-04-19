from django.db import models
from django.db.models import CheckConstraint, Q, F


class Account(models.Model):
    account_id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=100)
    username = models.CharField(max_length=60)
    password = models.CharField(max_length=60)
    created_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60)
    color = models.CharField(max_length=60)
    account_id = models.ForeignKey(Account, on_delete = models.CASCADE)

    def __str__(self):
        return self.name

class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    account_id = models.ForeignKey(Account, on_delete = models.CASCADE)
    category_id = models.ForeignKey(Category, on_delete = models.CASCADE, null = True, blank = True)
    location = models.CharField(max_length=100)
    event_start_date = models.DateField()
    event_start_time = models.TimeField(auto_now=False, auto_now_add=False, null=True, blank=True) # can be null
    event_end_date = models.DateField(null=True, blank=True)
    event_end_time = models.TimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    created_on = models.DateTimeField(auto_now=True)
    class Meta:
        constraints = [
            CheckConstraint(
                check = Q(event_end_date__gte=F('event_start_date')), # end date must be greater than start date (using __gt)
                name = 'check_start_date',
            ),
            CheckConstraint(
                check = Q(event_end_time__isnull = True) | Q(event_end_date__isnull = False), # if end date is null then end time must also be null
                name = 'check_end_time'
            )
        ]

    def __str__(self):
        return self.name
    
class Task(models.Model):
    task_id = models.AutoField(primary_key=True)
    account_id = models.ForeignKey(Account, on_delete = models.CASCADE)
    category_id = models.ForeignKey(Category, on_delete = models.CASCADE, null = True, blank = True)
    event_id = models.ForeignKey(Event, on_delete = models.CASCADE, null = True, blank = True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    due_date = models.DateField()
    due_time = models.TimeField(auto_now=False, auto_now_add=False, null = True, blank = True)
    completed = models.BooleanField()
    created_on = models.DateTimeField(auto_now=True)

