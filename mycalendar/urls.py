from django.urls import path
from . import views
from .views import edit

app_name = 'mycalendar'
urlpatterns = [
    path('', views.MonthCalendar.as_view(), name='month'),
    path('month/<int:year>/<int:month>/', views.MonthCalendar.as_view(), name='month'),
    path('week/', views.WeekCalendar.as_view(), name='week'),
    path('week/<int:year>/<int:month>/<int:day>/', views.WeekCalendar.as_view(), name='week'),

    path('month_with_schedule/', views.MonthWithScheduleCalendar.as_view(), name='month_with_schedule'),
    path('month_with_schedule/<int:year>/<int:month>/',
         views.MonthWithScheduleCalendar.as_view(), name='month_with_schedule'),

    path('month_with_forms/', views.MonthWithFormsCalendar.as_view(), name='month_with_forms'),
    path('month_with_forms/<int:year>/<int:month>/',
         views.MonthWithFormsCalendar.as_view(), name='month_with_forms'),

    path('week_with_schedule/', views.WeekWithScheduleCalendar.as_view(), name='week_with_schedule'),
    path('week_with_schedule/<int:year>/<int:month>/<int:day>/',
         views.WeekWithScheduleCalendar.as_view(), name='week_with_schedule'),

    path('business_calendar/', views.BusinessCalendar.as_view(), name='business_calendar'),
    path('business_calendar/<int:year>/<int:month>/<int:day>/',
         views.BusinessCalendar.as_view(), name='business_calendar'),

    path('edit/<int:num>', views.edit, name='edit'),
    path('delete/<int:num>', views.delete, name='delete'),

]
