from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import render

def renderSocket(request):
    return render(request, 'webSocket.html')


def renderInfo(request):
    return render(request, 'info.html')