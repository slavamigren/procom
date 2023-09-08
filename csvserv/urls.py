from django.urls import path
from csvserv.apps import CsvservConfig
from csvserv.views import CsvCreateView, CsvListView, CsvDetailView, CsvDeleteView

app_name = CsvservConfig.name

urlpatterns = [
    path('upload/', CsvCreateView.as_view(), name='upload'),
    path('list/', CsvListView.as_view(), name='list'),
    path('detail/<pk>/', CsvDetailView.as_view(), name='detail'),
    path('delete/<pk>/', CsvDeleteView.as_view(), name='delete'),
]