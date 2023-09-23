from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from csv_generator.models import (
    DataSchema,
    SchemaColumn,
    GeneratedCSV,
)

SCHEMA_LIST = reverse("csv_generator:schema-list")

SCHEMA_CREATE = reverse("csv_generator:schema-create")
SCHEMA_UPDATE = reverse(
    "csv_generator:schema-update", args="1"
)
SCHEMA_DELETE = reverse(
    "csv_generator:schema-delete", args="1"
)

CSV_GENERATE = reverse(
    "csv_generator:csv-generate", args="1"
)
CSV_DOWNLOAD = reverse(
    "csv_generator:csv-download", args="1"
)


class ViewsTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test1user",
            password="usertest123456",
        )

        self.client.force_login(self.user)

        self.data_schema = DataSchema.objects.create(
            title="test data schema",
            user=self.user,
        )
        self.schema_column_job = SchemaColumn.objects.create(
            name="Test job",
            type="Job",
            order=1,
            schema=self.data_schema,
        )
        self.schema_column_text = SchemaColumn.objects.create(
            name="Test text",
            type="Text",
            order=2,
            schema=self.data_schema,
        )
        self.generated_csv_file = GeneratedCSV.objects.create(
            file="Test file",
            data_schema=self.data_schema
        )

    def test_schema_update_right_id_required(self):
        hacker = get_user_model().objects.create_user(
            username="hacker",
            password="usertest123456",
        )

        self.client.force_login(hacker)
        response = self.client.get(SCHEMA_UPDATE)

        self.assertNotEquals(response.status_code, 200)

    def test_csv_generate_right_id_required(self):
        hacker = get_user_model().objects.create_user(
            username="hacker",
            password="usertest123456",
        )

        self.client.force_login(hacker)
        response = self.client.get(CSV_GENERATE)

        self.assertNotEquals(response.status_code, 200)

    def test_csv_download_right_id_required(self):
        hacker = get_user_model().objects.create_user(
            username="hacker",
            password="usertest123456",
        )

        self.client.force_login(hacker)
        response = self.client.get(CSV_DOWNLOAD)

        self.assertNotEquals(response.status_code, 200)