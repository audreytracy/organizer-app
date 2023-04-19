# Generated by Django 4.1.7 on 2023-04-18 23:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizer', '0001_initial'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='event',
            constraint=models.CheckConstraint(check=models.Q(('event_end_date__gt', models.F('event_start_date'))), name='check_start_date'),
        ),
        migrations.AddConstraint(
            model_name='event',
            constraint=models.CheckConstraint(check=models.Q(('event_end_time__isnull', True), ('event_end_date__isnull', False), _connector='OR'), name='check_end_time'),
        ),
    ]
