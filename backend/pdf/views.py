import PyPDF2
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from .models import PDFData
from .serializers import PDFDataSerializer

# Download necessary NLTK resources
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger_eng')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')

class UploadPDF(APIView):
    parser_classes = (MultiPartParser, FormParser)
    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB file size limit (adjust as needed)

    def post(self, request, *args, **kwargs):
        # Check if file is provided
        if 'file' not in request.FILES:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

        file = request.FILES['file']
        email = request.data.get('email')

        # Enforce file size limit
        if file.size > self.MAX_FILE_SIZE:
            return Response({'error': 'File size exceeds limit (5MB)'}, status=status.HTTP_400_BAD_REQUEST)

        # Initialize variables to store extracted text
        text = ''
        try:
            pdf_reader = PyPDF2.PdfReader(file)

            # Process PDF page by page (lazy loading)
            for page_num in range(len(pdf_reader.pages)):
                page_text = pdf_reader.pages[page_num].extract_text()
                text += page_text

        except Exception as e:
            return Response({'error': 'Error reading PDF'}, status=status.HTTP_400_BAD_REQUEST)

        # Tokenize and filter words
        words = word_tokenize(text)
        stop_words = set(stopwords.words('english'))

        # Use list comprehensions to filter words
        nouns = [word for word in words if word.isalpha() and word not in stop_words and nltk.pos_tag([word])[0][1] == 'NN']
        verbs = [word for word in words if word.isalpha() and word not in stop_words and nltk.pos_tag([word])[0][1] == 'VB']

        # Save data to the database
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
