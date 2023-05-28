# views.py

from django.http import HttpResponse
from django.shortcuts import redirect, render
from urllib import parse
from rest_framework.generics import GenericAPIView

import json
import os
from rest_framework.response import Response



REDIRECT_URI = os.getenv('REDIRECT_URI')
AUTHORIZATION_BASE_URL = os.getenv('AUTHORIZATION_BASE_URL')
TOKEN_URL = os.getenv('TOKEN_URL')
SCOPE = os.getenv('SCOPE')
API_EVENTS_URL = os.getenv('API_EVENTS_URL')




class InitView(GenericAPIView):
    def get(self, request):
        return render(request,'promt.html')
    

class GoogleCalendarInitView(GenericAPIView):
    def get(self, request):
        id = request.GET.get('id')
        key = request.GET.get('key')
        global CLIENT_ID
        global CLIENT_SECRET
        if id is None:
            CLIENT_ID = os.getenv('CLIENT_ID')
        else:
            CLIENT_ID = id
        if key is None:
            CLIENT_SECRET = os.getenv('CLIENT_SECRET')
        else:
            CLIENT_SECRET = key
        params = {
            'client_id': CLIENT_ID,
            'redirect_uri': REDIRECT_URI,
            'scope': SCOPE,
            'response_type': 'code',
        }
        authorization_url = AUTHORIZATION_BASE_URL + '?' + parse.urlencode(params)
        if key is not None:
            return Response({'data':authorization_url},status=200)
        return redirect(authorization_url)


class GoogleCalendarRedirectView(GenericAPIView):
    def get(self, request):
        # import pdb;pdb.set_trace()
        code = request.GET.get('code')
        data = {
            'code': code,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'redirect_uri': REDIRECT_URI,
            'grant_type': 'authorization_code',
        }
        data = parse.urlencode(data).encode()
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        import urllib.request as request
        
        # Exchange authorization code for access token
        req = request.Request(TOKEN_URL, data=data, headers=headers)
        response = request.urlopen(req)
        token_info = json.loads(response.read().decode())
        
        access_token = token_info.get('access_token')
        
        # Retrieve events from the user's calendar
        headers = {'Authorization': f'Bearer {access_token}'}
        req = request.Request(API_EVENTS_URL, headers=headers)
        response = request.urlopen(req)
        events = json.loads(response.read().decode()).get('items', [])
        
        # Display the list of events
        response = '<h2>Events:</h2>'
        if not events:
            response += '<p>No upcoming events found.</p>'
        else:
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                response += f'<p>{start} - {event["summary"]}</p>'
        
        return HttpResponse(response)
