import json

from django.contrib.auth import get_user_model
from django.http.response import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from chat.models import Chat


@csrf_exempt
def message_save(request):
    if request.method == 'POST':
        msg = request.POST.get('msgValue', None)
        user_id = request.POST.get('user_id', None)
        user = get_user_model().objects.get(id=user_id)
        chat = Chat(user=user, message=msg)
        if msg or msg != '':
            chat.save()
        return JsonResponse({'msg': msg, 'user': chat.user.username})


def get_messages(request):
    chats = Chat.objects.all()
    return render(request, 'chat/chat_list.html', {'chat': chats})
