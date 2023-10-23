"""PubSub target sink class, which handles writing streams."""

from __future__ import annotations
import json

from concurrent import futures
from google.cloud import pubsub_v1


from singer_sdk.sinks import BatchSink
from singer_sdk.target_base import Target


class CloudPubSubSink(BatchSink):
    """PubSub target sink class."""

    def __init__(
        self,
        target: Target,
        stream_name: str,
        schema: dict,
        key_properties: list[str] | None,
    ) -> None:
        super().__init__(target, stream_name, schema, key_properties)

        self.publisher = pubsub_v1.PublisherClient()
        self.topic_path = self.publisher.topic_path(
            self.config["project_id"], self.config["topic"]
        )

    def process_batch(self, context: dict) -> None:
        res = []
        for record in context["records"]:
            fut = self.publisher.publish(self.topic_path, json.dumps(record).encode("utf-8"))
            res.append(fut)

        futures.wait(res, return_when=futures.ALL_COMPLETED)
