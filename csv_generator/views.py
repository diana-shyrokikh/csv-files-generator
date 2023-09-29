import os

from django.conf import settings
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    AccessMixin,
)
from django.core.exceptions import PermissionDenied
from django.http import FileResponse
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)
from django.urls import reverse_lazy, reverse
from django.views import View, generic
from django.views.generic import ListView, CreateView

from csv_generator.forms import (
    DataSchemaForm,
    SchemaColumnFormSet,
)
from csv_generator.models import (
    DataSchema,
    GeneratedCSV,
)


class RightUserForDataSchemaRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        pk = kwargs.get("pk")

        data_schema = get_object_or_404(DataSchema, id=pk)

        if request.user.id != data_schema.user.id:
            if self.raise_exception:
                raise PermissionDenied
            else:
                return redirect(reverse("csv_generator:schema-list"))

        return super(RightUserForDataSchemaRequiredMixin, self).dispatch(
            request, *args, **kwargs
        )


class RightUserForCSVFileRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        generated_csv_file = get_object_or_404(GeneratedCSV, id=pk)

        if request.user.id != generated_csv_file.data_schema.user.id:
            if self.raise_exception:
                raise PermissionDenied
            else:
                return redirect(reverse("csv_generator:schema-list"))

        return super(RightUserForCSVFileRequiredMixin, self).dispatch(
            request, *args, **kwargs
        )


class DataSchemaListView(
    LoginRequiredMixin,
    ListView,
):
    model = DataSchema
    template_name = "data_schema_list.html"
    context_object_name = "data_schemas"

    def get_queryset(self):
        return DataSchema.objects.filter(
            user=self.request.user
        )


class DataSchemaCreateView(
    LoginRequiredMixin,
    CreateView,
):
    model = DataSchema
    form_class = DataSchemaForm
    template_name = "schema_form.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        if self.request.POST:
            data["children"] = SchemaColumnFormSet(
                self.request.POST, prefix="schema_column"
            )
        else:
            data["children"] = SchemaColumnFormSet(
                prefix="schema_column"
            )
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        children = context["children"]
        self.object = form.save()

        if children.is_valid():
            children.instance = self.object
            children.save()

            return super().form_valid(form)
        else:
            return self.render_to_response(context)

    def get_success_url(self):
        return reverse(
            "csv_generator:csv-generate",
            kwargs={'pk': self.object.pk}
        )


class DataSchemaUpdateView(
    LoginRequiredMixin,
    RightUserForDataSchemaRequiredMixin,
    generic.UpdateView,
):
    model = DataSchema
    form_class = DataSchemaForm
    template_name = "schema_form.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        if self.request.POST:
            data["children"] = SchemaColumnFormSet(
                self.request.POST, instance=self.object, prefix="schema_column"
            )
        else:
            data["children"] = SchemaColumnFormSet(
                instance=self.object,
                prefix="schema_column"
            )
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        children = context["children"]
        self.object = form.save()

        if children.is_valid():
            children.instance = self.object
            children.save()

            return super().form_valid(form)
        else:
            return self.render_to_response(context)

    def get_success_url(self):
        return reverse(
            "csv_generator:csv-generate",
            kwargs={'pk': self.object.pk}
        )


class DataSchemaDeleteView(
    LoginRequiredMixin,
    RightUserForDataSchemaRequiredMixin,
    generic.DeleteView,
):
    model = DataSchema
    template_name = "data_schema_confirm_delete.html"
    success_url = reverse_lazy("csv_generator:schema-list")


class CSVGenerateView(
    LoginRequiredMixin,
    RightUserForDataSchemaRequiredMixin,
    View,
):
    @staticmethod
    def get(request, pk):
        data_schema = DataSchema.objects.get(id=pk)
        generated_csv_files = GeneratedCSV.objects.filter(
            data_schema_id=pk
        )
        context = {
            "data_schema": data_schema,
            "generated_csv_files": generated_csv_files
        }

        return render(request, "generator_csv.html", context)


class CSVDownloadView(
    LoginRequiredMixin,
    RightUserForCSVFileRequiredMixin,
    View,
):
    @staticmethod
    def get(request, pk):
        csv_file = GeneratedCSV.objects.get(pk=pk)
        file_path = os.path.join(
            settings.MEDIA_ROOT, csv_file.file.name
        )
        filename = f"{csv_file.data_schema.title}.csv"
        response = FileResponse(
            open(file_path, "rb"),
            as_attachment=True,
        )
        response[
            "Content-Disposition"
        ] = f"attachment; filename={filename}"

        return response
