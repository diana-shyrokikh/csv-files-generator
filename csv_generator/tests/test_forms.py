from django.contrib.auth import get_user_model
from django.test import TestCase

from csv_generator.forms import (
    DataSchemaForm,
    SchemaColumnForm,
    SchemaColumnFormSet,
)
from csv_generator.models import DataSchema


class FormsTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="user1test",
            password="user123456"
        )
        self.data_schema = DataSchema.objects.create(
            title="test data schema",
            user=self.user,
        )

    def test_data_schema_form_valid(self):
        form_data = {
            "title": "Test title",
            "user": self.user
        }

        form = DataSchemaForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEquals(form.cleaned_data, form_data)

    def test_data_schema_form_not_valid(self):
        form_data = {
            "title": "1Test title",
            "user": self.user
        }

        form = DataSchemaForm(data=form_data)

        self.assertFalse(form.is_valid())

    def test_schema_column_form_valid(self):
        form_data = {
            "name": "Test job",
            "type": "Job",
            "order": 1,
            "from_range": None,
            "to_range": None,
            "schema": self.data_schema
        }

        form = SchemaColumnForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEquals(form.cleaned_data, form_data)

    def test_schema_column_form_not_valid(self):
        form_data = {
            "name": "Test job",
            "type": "Job",
            "order": -10,
            "from_range": None,
            "to_range": None,
            "schema": self.data_schema
        }

        form = SchemaColumnForm(data=form_data)

        self.assertFalse(form.is_valid())

    def test_schema_column_formset_valid(self):
        form_data = {
            "schema_columns-INITIAL_FORMS": 0,
            "schema_columns-TOTAL_FORMS": 2,
            "schema_columns-MAX_NUM_FORMS": None,

            "schema_columns-0-name": "Test job",
            "schema_columns-0-type": "Job",
            "schema_columns-0-order": 1,
            "schema_columns-0-from_range": None,
            "schema_columns-0-to_range": None,
            "schema_columns-0-DELETE": False,

            "schema_columns-1-name": "Test integer",
            "schema_columns-1-type": "Integer",
            "schema_columns-1-order": 2,
            "schema_columns-1-from_range": 5,
            "schema_columns-1-to_range": 10,
            "schema_columns-1-DELETE": False,

        }

        form = SchemaColumnFormSet(
            data=form_data,
            instance=self.data_schema
        )

        self.assertTrue(form.is_valid())

    def test_schema_column_formset_not_valid(self):
        form_data = {
            "schema_columns-INITIAL_FORMS": 0,
            "schema_columns-TOTAL_FORMS": 2,
            "schema_columns-MAX_NUM_FORMS": None,

            "schema_columns-0-name": "Test job",
            "schema_columns-0-type": "Job",
            "schema_columns-0-order": 1,
            "schema_columns-0-from_range": None,
            "schema_columns-0-to_range": None,
            "schema_columns-0-DELETE": False,

            "schema_columns-1-name": "Test integer",
            "schema_columns-1-type": "Integer",
            "schema_columns-1-order": 2,
            "schema_columns-1-from_range": 5,
            "schema_columns-1-to_range": 1,
            "schema_columns-1-DELETE": False,
        }

        form = SchemaColumnFormSet(
            data=form_data,
            instance=self.data_schema
        )

        self.assertFalse(form.is_valid())
