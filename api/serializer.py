from rest_framework import fields, serializers
from profile_app.models import book

class BookSerializer(serializers.ModelSerializer):
     
    class Meta:
        model = book
        fields = '__all__'