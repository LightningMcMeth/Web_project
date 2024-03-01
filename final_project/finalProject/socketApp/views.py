from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import render, redirect
import os

def renderSocket(request):
    return render(request, 'webSocket.html')

def wrongUrl(request):
    return redirect('getFileNames')

def renderInfo(request):
    return render(request, 'info.html')
