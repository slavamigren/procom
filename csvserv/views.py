from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from csvserv.models import CsvModel
from csvserv.serializers import CreateCsvSerializer, ListCsvSerializer, DetailCsvSerializer, DeleteCsvSerializer
import os
from rest_framework import response, status

class CsvCreateView(CreateAPIView):
    """Upload file view"""
    serializer_class = CreateCsvSerializer
    parser_classes = (MultiPartParser, FormParser)
    queryset = CsvModel.objects.all()

    def perform_create(self, serializer):
        """Add information about user and original file name"""
        uploaded_file = serializer.validated_data["file"]
        new_file = serializer.save()
        new_file.owner = self.request.user
        new_file.file_name = uploaded_file  # save file name, due to it can be changed by database
        self.pk = new_file.pk
        new_file.save()

    def create(self, request, *args, **kwargs):
        """Create and return id of the uploaded file"""
        super().create(request, *args, **kwargs)
        return response.Response({"id": self.pk}, status=status.HTTP_201_CREATED)


class CsvListView(ListAPIView):
    """Files list with fields"""
    serializer_class = ListCsvSerializer
    queryset = CsvModel.objects.all()


class CsvDetailView(RetrieveAPIView):
    """
    Files list view
    POST request has to have context data, for example:
    {
        "sort": {
            "Released_Year": false,
            "IMDB_Rating": true
        },
        "filter":{
            "Genre": "Drama",
            "Meta_score": "77"
        }
    }
    Data will be filtered by fields "Genre" and "Genre", after data will be sorted by
    fields "Released_Year" (not reversed) and "IMDB_Rating" (reversed)
    You can use any amount of fields for sorting and filtering or pass it.
    """
    serializer_class = DetailCsvSerializer
    queryset = CsvModel.objects.all()


class CsvDeleteView(DestroyAPIView):
    """Files delete view"""
    serializer_class = DeleteCsvSerializer
    queryset = CsvModel.objects.all()

    def perform_destroy(self, instance):
        file_path = instance.file.path
        super().perform_destroy(instance)
        os.remove(file_path)  # remove the file from filesystem

