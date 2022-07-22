# Generated by Django 3.0.4 on 2022-07-20 01:55

import datetime
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('summary', models.CharField(max_length=50, null=True, verbose_name='Summary')),
                ('description', models.TextField(blank=True, verbose_name='details')),
                ('start_time', models.TimeField(default=datetime.time(7, 0), verbose_name='start time')),
                ('end_time', models.TimeField(default=datetime.time(7, 0), verbose_name='end time')),
                ('date', models.DateField(verbose_name='date')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='create date')),
            ],
        ),
    ]
