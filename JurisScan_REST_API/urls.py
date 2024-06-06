from django.urls import path
from .views import UploadFileView, GetUserFilesView

urlpatterns = [
    path('upload/', UploadFileView.as_view(), name='file-upload'),
    path('get_user_files/<str:user_id>/', GetUserFilesView.as_view(), name='get-user-files'),
]
