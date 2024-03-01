from django.urls import path
from fileStorage import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('uploadFile/', views.uploadFile, name='uploadFile'),
    path('viewFiles/', views.getListOfFileNames, name='getFileNames'),
    path('success/', views.renderSuccess, name='success'),
    path('err/<str:errMsg>', views.customError, name='customError'),
    path('updateMetadata/<str:fileName>/', views.updateFileMetadata, name='updateMetadata'),
    path('deleteFile/<str:fileName>/', views.deleteFile, name='deleteFile'),
    path('downloadFile/<str:fileName>', views.downloadFile, name='downloadFile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])