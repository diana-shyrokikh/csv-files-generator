import csv
import json
import os
import uuid

from celery import shared_task
from django.conf import settings

from csv_generator.fake_data_generator import write_rows


@shared_task
def create_generated_csv_instance(data_schema_id):
    from csv_generator.models import DataSchema, GeneratedCSV

    data_schema = DataSchema.objects.get(id=data_schema_id)

    generated_csv_file = GeneratedCSV.objects.create(
        data_schema=data_schema
    )
    generated_csv_file.save()

    return {
        "type":
            "csv_generator_processing",
        "csv_instance_created":
            generated_csv_file.created.strftime("%Y-%m-%d"),
        "csv_instance_status":
            generated_csv_file.status,
        "csv_instance_id":
            generated_csv_file.id,
    }


@shared_task
def generate_csv_file(data_schema_id, csv_file_id, rows):
    from csv_generator.models import DataSchema, GeneratedCSV

    data_schema = DataSchema.objects.get(id=data_schema_id)
    columns = data_schema.schema_columns.order_by("order")
    field_names = list(
        columns.values_list("name", flat=True)
    )
    file_title = data_schema.title.replace(" ", "_")

    csv_file_name = f"{file_title}-{uuid.uuid4()}.csv"
    csv_file_path = os.path.join(
        settings.MEDIA_ROOT, csv_file_name
    )

    with open(
            csv_file_path,
            mode="w",
            newline=""
    ) as csv_file:
        csv_writer = csv.DictWriter(
            csv_file, fieldnames=field_names
        )

        csv_writer.writeheader()

        write_rows(rows, columns, csv_writer)

    generated_csv_file = GeneratedCSV.objects.get(id=csv_file_id)

    generated_csv_file.file = csv_file_name
    generated_csv_file.status = "Ready"
    generated_csv_file.save()

    return json.dumps({
        "type":
            "csv_generator_ready",
        "csv_instance_created":
            generated_csv_file.created.strftime("%Y-%m-%d"),
        "csv_instance_status":
            generated_csv_file.status,
        "csv_instance_id":
            generated_csv_file.id,
    })
