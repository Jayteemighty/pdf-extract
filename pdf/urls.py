from django.urls import path
from .views import UploadPDF

urlpatterns = [
    path('upload/', UploadPDF.as_view(), name='upload_pdf'),
]
