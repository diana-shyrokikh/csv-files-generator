from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from datetime import datetime

from csv_generator.models import (
    DataSchema,
    SchemaColumn,
    GeneratedCSV,
)


class ModelsTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="user123",
            password="user123465"
        )
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

    def test_user_str(self):
        self.assertEquals(str(self.user), self.user.username)

    def test_data_schema_str(self):
        self.assertEquals(
            str(self.data_schema),
            f"{self.data_schema.title} user: {self.data_schema.user}"
        )

    def test_schema_column_str(self):
        self.assertEquals(
            str(self.schema_column_job),
            f"Test job [Job]"
        )

    def test_generated_csv_str(self):
        self.assertEquals(
            str(self.generated_csv_file),
            "Test file"
        )

    def test_username_user_validation(self):
        usernames = ["123user", "123 user"]

        for username in usernames:
            with self.assertRaises(ValidationError):
                get_user_model().objects.create_user(
                    username=username,
                    password="user123465"
                )

    def test_title_data_schema_validation(self):
        titles = ["123dataschema", "dataschema_"]

        for title in titles:
            with self.assertRaises(ValidationError):
                DataSchema.objects.create(
                    title=title,
                    user=self.user,
                )

    def test_schema_column_validation(self):
        names = ["name(963", "68465"]

        for i in range(len(names)):
            with self.assertRaises(ValidationError):
                SchemaColumn.objects.create(
                    name=names[i],
                    type="Text",
                    order=i + 10,
                    schema=self.data_schema,
                )

        with self.assertRaises(ValidationError):
            SchemaColumn.objects.create(
                name="Test integer",
                type="Integer",
                order=40,
                from_range=-10,
                schema=self.data_schema,
            )

        with self.assertRaises(ValidationError):
            SchemaColumn.objects.create(
                name="Test integer",
                type="Integer",
                order=50,
                from_range=5,
                to_range=1,
                schema=self.data_schema,
            )

    def test_user(self):
        self.assertEquals(self.user.username, "user123")
        self.assertTrue(self.user.check_password("user123465"))

    def test_data_schema(self):
        self.assertEquals(self.data_schema.title, "test data schema" )
        self.assertEquals(self.data_schema.user, self.user)
        self.assertEquals(self.data_schema.modified, datetime.now().date())

    def test_schema_column(self):
        self.assertEquals(
            self.schema_column_text.name, "Test text"
        )
        self.assertEquals(
            self.schema_column_text.type, "Text"
        )
        self.assertEquals(
            self.schema_column_text.order, 2
        )
        self.assertEquals(
            self.schema_column_text.schema, self.data_schema
        )
        self.assertEquals(
            self.schema_column_text.from_range, 1
        )
        self.assertEquals(
            self.schema_column_text.to_range, 2
        )
