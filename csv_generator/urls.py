from django.urls import path

from csv_generator.views import DataSchemaListView

app_name = "csv_generator"

urlpatterns = [
    path("schemas/", DataSchemaListView.as_view(), name="data_schemas"),
]
