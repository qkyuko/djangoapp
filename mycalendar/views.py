
import datetime
from pipes import Template
from sqlite3 import paramstyle
from traceback import StackSummary
from django.shortcuts import redirect, render
from django.views import generic
from .forms import BS4ScheduleForm, SimpleScheduleForm
from .models import Schedule
from . import mixins
from django.utils import timezone
import pytz


class MonthCalendar(mixins.MonthCalendarMixin, generic.TemplateView):
    #月間カレンダーを表示するビュー
    template_name = 'mycalendar/month.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)
        return context

class WeekCalendar(mixins.WeekCalendarMixin, generic.TemplateView):
    #週間カレンダーを表示するビュー
    template_name = 'mycalendar/week.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_week_calendar()
        context.update(calendar_context)
        return context

class WeekWithScheduleCalendar(mixins.WeekWithScheduleMixin, generic.TemplateView):
    #スケジュール付きの週間カレンダーを表示するビュー
    template_name = 'mycalendar/week_with_schedule.html'
    model = Schedule
    date_field = 'date'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_week_calendar()
        context.update(calendar_context)
        context['week_row'] = zip(
            calendar_context['week_names'],
            calendar_context['week_days'],
            calendar_context['week_day_schedules'].values()
        )
        return context


class MonthWithScheduleCalendar(mixins.MonthWithScheduleMixin, generic.TemplateView):
    #スケジュール付きの月間カレンダーを表示するビュー
    template_name = 'mycalendar/month_with_schedule.html'
    model = Schedule
    date_field = 'date'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)
        return context
    
class MonthWithFormsCalendar(mixins.MonthWithFormsMixin, generic.View):
    #フォーム付きの月間カレンダーを表示するビュー
    template_name = 'mycalendar/month_with_forms.html'
    model = Schedule
    date_field = 'date'
    form_class = SimpleScheduleForm
    

    def get(self, request, **kwargs):
        context = self.get_month_calendar()
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        context = self.get_month_calendar()
        formset = context['month_formset']
        if formset.is_valid():
            formset.save()
            return redirect('mycalendar:month_with_forms')

        return render(request, self.template_name, context)



class BusinessCalendar(mixins.MonthCalendarMixin, mixins.WeekWithScheduleMixin, generic.CreateView):
    #月間カレンダー、週間カレンダー、スケジュール登録画面付

    template_name = 'mycalendar/business_calendar.html'
    model = Schedule
    date_field = 'date'
    form_class = BS4ScheduleForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        week_calendar_context = self.get_week_calendar()
        month_calendar_context = self.get_month_calendar()
        context.update(week_calendar_context)
        context.update(month_calendar_context)
        return context  



    def form_valid(self, form):
        month = self.kwargs.get('month')
        year = self.kwargs.get('year')
        day = self.kwargs.get('day')
        if month and year and day:
            date = datetime.date(year=int(year), month=int(month), day=int(day))
        else:
            date = datetime.date.today()
        schedule = form.save(commit=False)
        schedule.date = date
        schedule.save()
        return redirect('mycalendar:business_calendar', year=date.year, month=date.month, day=date.day)
    
def edit(request, num):
    obj = Schedule.objects.get(id=num)
    if (request.method == 'POST'):
        schedule = BS4ScheduleForm(request.POST, instance=obj)
        schedule.save()
        return redirect(to='/mycalendar/business_calendar')
    params = {
        'title': 'Mycalendar',
        'id': num,
        'form': BS4ScheduleForm(instance=obj),
    }
    return render(request, 'mycalendar/edit.html', params)

def delete(request, num):
    obj = Schedule.objects.get(id=num)
    if (request.method == 'POST'):
        schedule = BS4ScheduleForm(request.POST, instance=obj)
        schedule.delete()
        return redirect(to='/business_calendar')
    params = {
        'title': 'Mycalendar',
        'id':num,
        'form': BS4ScheduleForm(instance=obj)
    }
    return render(request, 'mycalendar/delete.html', params)


def top(request):
    context = {
        'now': timezone.now(),
        'timzones': pytz.common_timezones,

    } 
    return render(request, 'mycalendar/top.html', context)
      

    
    