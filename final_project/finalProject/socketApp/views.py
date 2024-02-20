from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import render
import os

def renderSocket(request):
    return render(request, 'webSocket.html')


def renderInfo(request):
    return render(request, 'info.html')

def retrieveFileInfo(request):
    #implement retrieval of the file name and stuff from the request
    path = 'pathtothefileandstuff/dot/com' # + request data

    size = os.path.getsize(path)
    lastModified = os.path.getmtime(path)
    creationTime = os.path.getctime(path)

    fileInfo = dict(size = size, lastModified = lastModified, creationTime = creationTime)