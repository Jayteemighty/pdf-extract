from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PDFData
from .serializers import PDFDataSerializer
import fitz  # PyMuPDF
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from django.core.files.storage import FileSystemStorage
import os

# Append the correct path to the nltk_data in the virtual environment
nltk.data.path.append('./venv/nltk_data/')

# Ensure NLTK resources are already downloaded
nltk.download('punkt', quiet=True, download_dir='./venv/nltk_data/')
nltk.download('averaged_perceptron_tagger', quiet=True, download_dir='./venv/nltk_data/')


class UploadPDF(APIView):
    def post(self, request):
        pdf_file = request.FILES.get('pdf')
        email = request.data.get('email')

        if not pdf_file or not email:
            return Response({"error": "Missing file or email"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Save the file to the server temporarily
            fs = FileSystemStorage()
            filename = fs.save(pdf_file.name, pdf_file)
            file_path = fs.path(filename)

            # Extract text from the saved PDF file
            doc = fitz.open(file_path)
            text = ""
            for page in doc:
                text += page.get_text()

            # Tokenize and POS tag the text
            words = word_tokenize(text)
            tagged = pos_tag(words)

            # Extract nouns and verbs
            nouns = [word for word, pos in tagged if pos.startswith('NN')]
            verbs = [word for word, pos in tagged if pos.startswith('VB')]

            # Save data to the database
            pdf_data = PDFData.objects.create(email=email, nouns=nouns, verbs=verbs)

            # Serialize and return data
            serializer = PDFDataSerializer(pdf_data)

            # Optionally, delete the file after processing
            if os.path.exists(file_path):
                os.remove(file_path)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
