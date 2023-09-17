from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from csv_generator.forms import DataSchemaForm, SchemaColumnFormSet
from csv_generator.models import DataSchema


class DataSchemaListView(ListView):
    model = DataSchema
    template_name = "data_schema_list.html"
    context_object_name = "data_schemas"

    def get_queryset(self):
        return DataSchema.objects.filter(user=self.request.user)


class DataSchemaCreateView(CreateView):
    model = DataSchema
    form_class = DataSchemaForm
    template_name = "schema_form.html"
    context_object_name = "new_schema"
    success_url = reverse_lazy("csv_generator:schema-list")

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["children"] = SchemaColumnFormSet(self.request.POST, prefix="schema_column")
        else:
            data["children"] = SchemaColumnFormSet(prefix="schema_column")
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        children = context["children"]
        self.object = form.save()
        if children.is_valid():
            children.instance = self.object
            children.save()
        return super().form_valid(form)
