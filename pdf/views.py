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

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

class UploadPDF(APIView):
    def post(self, request):
        pdf_file = request.FILES.get('pdf')
        email = request.data.get('email')

        if not pdf_file or not email:
            return Response({"error": "Missing file or email"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Extract text from PDF
            doc = fitz.open(pdf_file)
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
            pdf_data.save()

            # Serialize and return data
            serializer = PDFDataSerializer(pdf_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
