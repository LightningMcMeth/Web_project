from django.urls import path
from fileStorage import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('uploadFile/', views.uploadFile, name='uploadFile'),
    path('viewFiles/', views.getListOfFileNames, name='getFileNames'),
    path('success/', views.renderSuccess),
    path('updateMetadata/<str:fileName>/', views.updateFileMetadata, name='updateMetadata'),
    path('deleteFile/<str:fileName>/', views.deleteFile, name='deleteFile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])