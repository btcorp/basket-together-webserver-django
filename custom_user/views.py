from django.shortcuts import render, get_object_or_404, redirect
from time import timezone
# from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.http import HttpResponse, JsonResponse
import sys
import json, requests
import logging


logger = logging.getLogger('test')

def user_add(request):
    """
    # username = request.POST['username']
    # password = request.POST['password']
    # user = auth.authenticate(username=username, password=password)
    # return render(request, 'register.html', {'data': request.POST})
    if request.method == 'POST':
        return 'POST OK'
    json_data = json.loads(request.body)

    data =[
        {'json_data': json_data}
    ]
    # return JsonResponse(data, safe=False)
    """
    if request.method == 'POST':
        logger.debug(request)
        logger.error('-------------------------------no error-----------------------------')

    logger.error('-------------------------------error-----------------------------')
    data = [
        {'id':1, 'title':'title 1'}
    ]
    return JsonResponse(data, safe=False)

