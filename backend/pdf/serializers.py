from rest_framework import serializers
from .models import PDFData

class PDFDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = PDFData
        fields = ['email', 'nouns', 'verbs']
