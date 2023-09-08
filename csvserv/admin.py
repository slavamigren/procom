from django.contrib import admin

from csvserv.models import CsvModel


@admin.register(CsvModel)
class CsvAdmin(admin.ModelAdmin):
    list_display = ('pk', 'file_name', 'date_time', 'owner', )
