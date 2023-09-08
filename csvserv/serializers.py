import csv

from rest_framework import serializers

from csvserv.models import CsvModel
from csvserv.services import proceed_dict


class CreateCsvSerializer(serializers.ModelSerializer):
    """Upload a file"""
    class Meta:
        model = CsvModel
        fields = ['file']


class ListCsvSerializer(serializers.ModelSerializer):
    """Files list with fields"""
    file_fields = serializers.SerializerMethodField()

    class Meta:
        model = CsvModel
        fields = ['id', 'file_name', 'file_fields']

    def get_file_fields(self, instance):
        try:
            with open(instance.file.path, 'r', encoding='utf-8') as file:
                rows = csv.reader(file)
                try:
                    return next(rows)
                except StopIteration:
                    return 'file is empty'
        except:
            return 'bad file format'


class DetailCsvSerializer(serializers.ModelSerializer):
    """Returns file name and sorted-filtered data from file"""
    file_fields = serializers.SerializerMethodField()

    class Meta:
        model = CsvModel
        fields = ['id', 'file_name', 'file_fields']

    def get_file_fields(self, instance):
        try:
            with open(instance.file.path, 'r', encoding='utf-8') as file:
                rows = csv.DictReader(file)
                data = [i for i in rows]
                if not data:
                    return 'file is empty'
                if self.context.get('request', None):
                    data = proceed_dict(data, self.context['request'].data)
                return data
        except:
            return 'bad file format'

class DeleteCsvSerializer(serializers.ModelSerializer):
    """Delete file from database"""
    class Meta:
        model = CsvModel
        fields = '__all__'
