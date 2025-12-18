import json
import os
import pika


def publish_image_resize_event(post_id: int) -> None:
    rabbitmq_url = os.getenv(
        "RABBITMQ_URL",
        "amqp://guest:guest@rabbitmq:5672/"
    )

    params = pika.URLParameters(rabbitmq_url)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    channel.queue_declare(
        queue="image_resize",
        durable=True
    )

    message = json.dumps({"post_id": post_id})

    channel.basic_publish(
        exchange="",
        routing_key="image_resize",
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=2  # persist message
        )
    )

    connection.close()