from django.db import models

class Account(models.Model):
    account_id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=100)
    username = models.CharField(max_length=60)
    password = models.CharField(max_length=60)
    created_on = models.DateTimeField()

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
    category_id = models.ForeignKey(Category, on_delete = models.CASCADE)
    location = models.CharField(max_length=100)
    event_start_date = models.DateField()
    event_start_time = models.TimeField(auto_now=False, auto_now_add=False)
    event_end_date = models.DateField()
    event_end_time = models.TimeField(auto_now=False, auto_now_add=False)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    created_on = models.DateTimeField()

    def __str__(self):
        return self.name
    
class Task(models.Model):
    task_id = models.AutoField(primary_key=True)
    account_id = models.ForeignKey(Account, on_delete = models.CASCADE)
    category_id = models.ForeignKey(Category, on_delete = models.CASCADE)
    event_id = models.ForeignKey(Event, on_delete = models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    due_date = models.DateField()
    due_time = models.TimeField(auto_now=False, auto_now_add=False)
    completed = models.IntegerField()
    created_on = models.DateTimeField()

