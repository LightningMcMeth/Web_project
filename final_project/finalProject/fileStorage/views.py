import json
from datetime import datetime
import requests
from django.utils.timezone import make_aware
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from fileStorage import helpers
from django.conf import settings
import os


def uploadFile(request):

    if request.method == 'POST':
        form = helpers.FileUploadForm(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():

            name = form.cleaned_data['filename']
            uploadedFile = request.FILES['file']
            description = form.cleaned_data['fileDescription']

            pathToStorage = os.path.join(settings.BASE_DIR, 'fileStorage/filestorage')
            fs = FileSystemStorage(location=pathToStorage)
            realFilename, extension = os.path.splitext(uploadedFile.name)
            filepath = fs.save( name + extension, uploadedFile)
            print(filepath)

            size = uploadedFile.size
            lastAccessedDT = make_aware(datetime.fromtimestamp(os.path.getatime(fs.path(filepath))))
            lastModifiedDT = make_aware(datetime.fromtimestamp(os.path.getmtime(fs.path(filepath))))
            creationDT = make_aware(datetime.fromtimestamp(os.path.getctime(fs.path(filepath))))

            data = {
                'name': name,
                'creationDT': creationDT.isoformat(),
                'lastModifiedDT': lastModifiedDT.isoformat(),
                'lastAccessedDT': lastAccessedDT.isoformat(),
                'size': size,
                'description': description,
            }

            response = requests.put('http://localhost:3500/md/new', json=data)
            print(response.status_code)

            if response.status_code == 200:
                return HttpResponseRedirect('/fs/success/')

    else:
        form = helpers.FileUploadForm()
        print(form.errors)
    return render(request, 'uploadFile.html', {'form': form})


def getListOfFileNames(request):
    storageFolder = os.path.join(settings.BASE_DIR, 'fileStorage/filestorage')
    fileNames = os.listdir(storageFolder)

    filesWithDescriptions = []

    for file in fileNames:
        nameWithoutExtension = os.path.splitext(file)[0]
        response = requests.get(f'http://localhost:3500/md/getByName/{nameWithoutExtension}')
        if response.status_code == 200:
            metadataList = response.json()


            if metadataList:
                description = metadataList[0].get('description', 'No description available')
            else:
                description = 'No description available'
        else:
            description = 'Description not found'

        filesWithDescriptions.append({'name': file, 'description': description})

    return render(request, 'listFiles.html', {'files': filesWithDescriptions})


def updateFileMetadata(request, fileName):
    nameWithoutExtension, _ = os.path.splitext(fileName)

    if request.method == 'POST':
        description = request.POST.get('description')

        data = {'description': description}
        response = requests.put(f'http://localhost:3500/md/updateByName/{nameWithoutExtension}', json=data)
        if response.status_code != 200:
            print("bruh")

        return HttpResponseRedirect('/fs/success/')

    else:
        response = requests.get(f'http://localhost:3500/md/getByName/{nameWithoutExtension}')
        if response.status_code == 200:
            metadata = response.json()
        else:
            metadata = None

    return render(request, 'updateMetadata.html', {'metadata': metadata, 'fileName': fileName})



def deleteFile(request, fileName):
    nameTokens = fileName.rsplit('.', 1)
    nameWithoutExtension = nameTokens[0]
    print(nameWithoutExtension)
    storageFolder = os.path.join(settings.BASE_DIR, 'fileStorage/filestorage')
    filepath = os.path.join(storageFolder, fileName)

    if os.path.exists(filepath):
        os.remove(filepath)

    response = requests.delete(f'http://localhost:3500/md/deleteByName/{nameWithoutExtension}')
    if response.status_code != 200:
        print("bruh")

    return HttpResponseRedirect('/fs/success/')

def renderSuccess(request):
    return render(request, 'success.html')