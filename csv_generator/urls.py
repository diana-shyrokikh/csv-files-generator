from django.urls import path

from csv_generator.views import (
    DataSchemaListView,
    DataSchemaCreateView,
    CSVGenerateView,
    CSVDownloadView,
)

app_name = "csv_generator"

urlpatterns = [
    path(
        "",
        DataSchemaListView.as_view(),
        name="schema-list"
    ),
    path(
        "create/",
        DataSchemaCreateView.as_view(),
        name="schema-create"
    ),
    path(
        "generate/<int:pk>/",
        CSVGenerateView.as_view(),
        name="csv-generate"
    ),
    path(
        "generate/<int:pk>/download/",
        CSVDownloadView.as_view(),
        name="csv-download"
    ),
]
