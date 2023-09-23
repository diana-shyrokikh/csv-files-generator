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
        "",
        DataSchemaListView.as_view(),
        name="schema-list"
    ),
    path(
        "schema/create/",
        DataSchemaCreateView.as_view(),
        name="schema-create"
    ),
    path(
        "schema/update/<int:pk>/",
        DataSchemaUpdateView.as_view(),
        name="schema-update"
    ),
    path(
        "schema/delete/<int:pk>/",
        DataSchemaDeleteView.as_view(),
        name="schema-delete"
    ),
    path(
        "schema/generate/<int:pk>/",
        CSVGenerateView.as_view(),
        name="csv-generate"
    ),
    path(
        "schema/generate/<int:pk>/download/",
        CSVDownloadView.as_view(),
        name="csv-download"
    ),
    path(
        "accounts/",
        include("django.contrib.auth.urls")
    ),
]
