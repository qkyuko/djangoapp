import datetime
from pickle import FALSE
from django.db import models
from django.utils import timezone


# for schedule
class Schedule(models.Model):

    summary = models.CharField('Summary', max_length=50,null=True)
    description = models.TextField('details', blank=True)
    start_time = models.TimeField('start time', default=datetime.time(7, 0, 0))
    end_time = models.TimeField('end time', default=datetime.time(7, 0, 0))
    date = models.DateField('date')
    created_at = models.DateTimeField('create date', default=timezone.now)

    def __str__(self):
        return self.summary + ',Schedule_ID:' +str(self.id) 
