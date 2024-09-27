import PyPDF2
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from .models import PDFData
from .serializers import PDFDataSerializer

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')
import nltk

class UploadPDF(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        if 'file' not in request.FILES:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

        file = request.FILES['file']
        email = request.data.get('email')

        # Extract text from PDF
        pdf_reader = PyPDF2.PdfReader(file)
        text = ''
        for page_num in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page_num].extract_text()

        # Tokenize and filter words
        words = word_tokenize(text)
        stop_words = set(stopwords.words('english'))
        nouns = [word for word in words if word.isalpha() and word not in stop_words and nltk.pos_tag([word])[0][1] == 'NN']
        verbs = [word for word in words if word.isalpha() and word not in stop_words and nltk.pos_tag([word])[0][1] == 'VB']

        # Save to database
        data = {
            'email': email,
            'nouns': nouns,
            'verbs': verbs
        }
        serializer = PDFDataSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)