from django.urls import path

from csv_generator.views import DataSchemaListView, DataSchemaCreateView

app_name = "csv_generator"

urlpatterns = [
    path("schemas/", DataSchemaListView.as_view(), name="schema-list"),
    path("schemas/create/", DataSchemaCreateView.as_view(), name="schema-create"),
]
