from django.shortcuts import render
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from django.http.response import HttpResponse, JsonResponse
from . import serializer




# Create your views here.

class CreateBookAPI(CreateAPIView):
    # permission_classes = (IsAuthenticated,IsSchool)
    serializer_class = serializer.BookSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"message": "success"}, status=200)
        
        return JsonResponse({"message": str(e)}, status=404)






