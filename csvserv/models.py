from django.db import models
from conf import settings

NULLABLE = {'blank': True, 'null': True}


class CsvModel(models.Model):
    file = models.FileField(verbose_name='file')
    date_time = models.DateTimeField(auto_now_add=True, verbose_name='date and time uploaded')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE,
                              verbose_name='user')
    file_name = models.CharField(max_length=100, verbose_name='file_name')

    class Meta:
        verbose_name = 'file'
        verbose_name_plural = 'files'
        ordering = ('date_time',)

    def __str__(self):
        return f'{self.date_time}: {self.file_name}'
