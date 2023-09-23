from django.urls import path, include

from csv_generator.views import (
    DataSchemaListView,
    DataSchemaCreateView,
    DataSchemaUpdateView,
    DataSchemaDeleteView,
    CSVGenerateView,
    CSVDownloadView,
)

app_name = "csv_generator"

urlpatterns = [
    path(
        "home/",
        DataSchemaListView.as_view(),
        name="schema-list"
    ),
    path(
        "create/",
        DataSchemaCreateView.as_view(),
        name="schema-create"
    ),
    path(
        "update/<int:pk>/",
        DataSchemaUpdateView.as_view(),
        name="schema-update"
    ),
    path(
        "delete/<int:pk>/",
        DataSchemaDeleteView.as_view(),
        name="schema-delete"
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
    path(
        "accounts/",
        include("django.contrib.auth.urls")
    ),
]
