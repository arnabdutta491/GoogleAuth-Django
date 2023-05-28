# urls.py

from django.urls import path
from .views import *

urlpatterns = [
    path('',InitView.as_view(),name = 'promt-file'),
    path('rest/v1/calendar/init/', GoogleCalendarInitView.as_view(), name='google-calendar-init'),
    path('rest/v1/calendar/redirect/', GoogleCalendarRedirectView.as_view(), name='google-calendar-redirect'),
]
