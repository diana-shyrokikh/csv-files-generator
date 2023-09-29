import json
from channels.generic.websocket import WebsocketConsumer

from .tasks import (
    generate_csv_file,
    create_generated_csv_instance,
)


class CSVGeneratorConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

        self.send(text_data=json.dumps({
            "type": "connection_established",
            "message": "WebSocket connected"
        }))

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        rows = text_data_json.get("rows")
        data_schema_id = text_data_json.get("data_schema_id")
        csv = create_generated_csv_instance(data_schema_id)

        self.send(text_data=json.dumps(csv))
        self.send(text_data=generate_csv_file(
                data_schema_id,
                csv.get("csv_instance_id"),
                rows
        ))
