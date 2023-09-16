from django.shortcuts import render
from django.views.generic import ListView

from csv_generator.models import DataSchema


class DataSchemaListView(ListView):
    model = DataSchema
    template_name = "data_schema_list.html"
    context_object_name = "data_schemas"

    def get_queryset(self):
        return DataSchema.objects.filter(user=self.request.user)
