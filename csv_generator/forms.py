from django import forms
from django.forms import inlineformset_factory

from csv_generator.models import SchemaColumn, DataSchema


class SchemaColumnForm(forms.ModelForm):
    class Meta:
        model = SchemaColumn
        fields = "__all__"


class DataSchemaForm(forms.ModelForm):
    class Meta:
        model = DataSchema
        fields = "__all__"


SchemaColumnFormSet = inlineformset_factory(
    DataSchema,
    SchemaColumn,
    extra=10,
    fields="__all__",
)
