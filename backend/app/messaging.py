import json
import os
import pika
import logging


def _publish_event(queue_name: str, post_id: int) -> None:
    """Generic function to publish events to RabbitMQ"""
    rabbitmq_url = os.getenv(
        "RABBITMQ_URL",
        "amqp://guest:guest@rabbitmq:5672/"
    )

    try:
        params = pika.URLParameters(rabbitmq_url)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()

        channel.queue_declare(
            queue=queue_name,
            durable=True
        )

        message = json.dumps({"post_id": post_id})

        channel.basic_publish(
            exchange="",
            routing_key=queue_name,
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2  # persist message
            )
        )

        connection.close()

    except Exception as e:
        logging.warning(
            f"[messaging] RabbitMQ unavailable, skipping {queue_name} event: {e}"
        )


def publish_image_resize_event(post_id: int) -> None:
    """
    Publish image resize event.

    IMPORTANT:
    - This must NEVER break the REST API.
    - If RabbitMQ is unavailable (tests / CI), we silently skip.
    """
    _publish_event("image_resize", post_id)


def publish_sentiment_analysis_event(post_id: int) -> None:
    """Publish sentiment analysis event"""
    _publish_event("sentiment_analysis", post_id)


def publish_text_generation_event(post_id: int) -> None:
    """Publish text generation event"""
    _publish_event("text_generation", post_id)