from datetime import datetime
import json
import requests
from django.utils.timezone import make_aware
from django.urls import reverse
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from requests import RequestException

from fileStorage import helpers
from cryptography.fernet import Fernet
from io import BytesIO
import os
import logging

logger = logging.getLogger(__name__)

def storeKey(fileName, key):
    try:
        with open("fileStorage/keys/encryptionKeys.json", "r") as file:
            keys = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as err:
        keys = {}
        logger.error(f"Error loading encryption keys, file not found: {str(err)}")

    keys[fileName] = key.decode()

    with open("fileStorage/keys/encryptionKeys.json", "w") as file:
        json.dump(keys, file)


def retrieveKey(fileName):
    try:
        with open("fileStorage/keys/encryptionKeys.json", "r") as file:
            keys = json.load(file)

        if fileName in keys:
            return keys[fileName].encode()

    except (FileNotFoundError, json.JSONDecodeError) as err:
        logger.error(f"Error loading encryption keys, file not found: {str(err)}")

    return None


def generateKey():
    return Fernet.generate_key()


def encryptFile(fileContent, encryptionKey):
    fernet = Fernet(encryptionKey)
    return fernet.encrypt(fileContent)


def decryptFile(encryptedContent, encryptionKey):
    fernet = Fernet(encryptionKey)
    return fernet.decrypt(encryptedContent)


def uploadFile(request):

    if request.method == 'POST':
        form = helpers.FileUploadForm(request.POST, request.FILES)

        if form.is_valid():

            name = form.cleaned_data['filename']
            uploadedFile = request.FILES['file']
            description = form.cleaned_data['fileDescription']

            pathToStorage = os.path.join(settings.BASE_DIR, 'fileStorage/filestorage')
            fs = FileSystemStorage(location=pathToStorage)
            originalFilename, extension = os.path.splitext(uploadedFile.name)

            encryptionKey = generateKey()
            encryptedContent = encryptFile(uploadedFile.read(), encryptionKey)
            encryptedFile = BytesIO(encryptedContent)
            filepath = fs.save(name + extension, encryptedFile)

            storeKey(filepath, encryptionKey)

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

            if response.status_code == 200:
                return HttpResponseRedirect('/fs/success/')
            else:
                errMsg = f"Couldn't upload file metadata: code: {response.status_code}, {response.reason}"
                logger.error(errMsg)
                return redirect(reverse('customError', kwargs={'errMsg': errMsg}))

    else:
        form = helpers.FileUploadForm()

    return render(request, 'uploadFile.html', {'form': form})


def downloadFile(request, fileName):

    encryptionKey = retrieveKey(fileName)

    if not encryptionKey:
        logger.error(f"Couldn't find encryption key")
        return HttpResponse('Encryption key not found', status=404)

    pathToStorage = os.path.join(settings.BASE_DIR, 'fileStorage/filestorage')
    filepath = os.path.join(pathToStorage, fileName)

    if not os.path.exists(filepath):
        logger.error(f"Encrypted file wasn't found")
        return HttpResponse('File not found', status=404)

    with open(filepath, 'rb') as encryptedFile:
        encryptedContent = encryptedFile.read()
        decryptedContent = decryptFile(encryptedContent, encryptionKey)

    response = HttpResponse(decryptedContent, content_type='application/octet-stream')
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(fileName)
    return response


def getListOfFileNames(request):
    storageFolder = os.path.join(settings.BASE_DIR, 'fileStorage/filestorage')
    fileNames = os.listdir(storageFolder)

    filesWithDescriptions = []

    for file in fileNames:
        nameWithoutExtension = os.path.splitext(file)[0]
        try:
            response = requests.get(f'http://localhost:3500/md/getByName/{nameWithoutExtension}')
            #if response.status_code == 200:
            metadataList = response.json()

            if metadataList:
                description = metadataList[0].get('description', 'No description available')
            else:
                description = 'No description available'

        except RequestException as err:
            description = 'Description not found'

        filesWithDescriptions.append({'name': file, 'description': description})

    return render(request, 'listFiles.html', {'files': filesWithDescriptions})


def updateFileMetadata(request, fileName):
    nameWithoutExtension, _ = os.path.splitext(fileName)

    if request.method == 'POST':

        description = request.POST.get('description')
        data = {'description': description}

        try:
            response = requests.put(f'http://localhost:3500/md/updateByName/{nameWithoutExtension}', json=data)
        except RequestException as err:

        #if response.status_code != 200:

                errMsg = f"Couldn't upload file metadata: {str(err)}"
                logger.error(errMsg)
                return redirect(reverse('customError', kwargs={'errMsg': errMsg}))

        return HttpResponseRedirect('/fs/success/')

    else:
        try:

            response = requests.get(f'http://localhost:3500/md/getByName/{nameWithoutExtension}')

            if response.status_code == 200:
                metadata = response.json()

                for item in metadata:
                    item['size'] = f"{item['size'] / 1048576:.2f}"
                    item['lastAccessedDT'] = datetime.strptime(item['lastAccessedDT'], "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%B %d, %Y, %H:%M:%S")
                    item['lastModifiedDT'] = datetime.strptime(item['lastModifiedDT'], "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%B %d, %Y, %H:%M:%S")
                    item['creationDT'] = datetime.strptime(item['creationDT'], "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%B %d, %Y, %H:%M:%S")

        except RequestException as err:
            metadata = None
            errMsg = f"Couldn't retrieve file metadata: {str(err)}"
            logger.error(errMsg)

    return render(request, 'updateMetadata.html', {'metadata': metadata, 'fileName': fileName})


def deleteFile(request, fileName):
    nameTokens = fileName.rsplit('.', 1)
    nameWithoutExtension = nameTokens[0]

    storageFolder = os.path.join(settings.BASE_DIR, 'fileStorage/filestorage')
    filepath = os.path.join(storageFolder, fileName)

    if os.path.exists(filepath):
        os.remove(filepath)
    else:
        logger.error(f"Couldn't find and delete file")

    try:
        response = requests.delete(f'http://localhost:3500/md/deleteByName/{nameWithoutExtension}')
    except RequestException as err:

    #if response.status_code != 200:
        errMsg = f"Couldn't delete file metadata: {str(err)}"
        logger.error(errMsg)
        return redirect(reverse('customError', kwargs={'errMsg': errMsg}))

    return HttpResponseRedirect('/fs/success/')


def renderSuccess(request):
    return render(request, 'success.html')


def customError(request, errMsg):
    return render(request, 'customError.html', {'errMsg': errMsg})

