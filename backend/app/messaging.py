import json
import os
import pika
import logging


def publish_image_resize_event(post_id: int) -> None:
    """
    Publish image resize event.

    IMPORTANT:
    - This must NEVER break the REST API.
    - If RabbitMQ is unavailable (tests / CI), we silently skip.
    """

    rabbitmq_url = os.getenv(
        "RABBITMQ_URL",
        "amqp://guest:guest@rabbitmq:5672/"
    )

    try:
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

    except Exception as e:
        logging.warning(
            f"[messaging] RabbitMQ unavailable, skipping resize event: {e}"
        )


def publish_sentiment_analysis_event(post_id: int, text: str) -> None:
    """
    Publish sentiment analysis event.
    
    Args:
        post_id: ID of the post to analyze
        text: Text content to analyze
    
    IMPORTANT:
    - This must NEVER break the REST API.
    - If RabbitMQ is unavailable, we silently skip.
    """
    rabbitmq_url = os.getenv(
        "RABBITMQ_URL",
        "amqp://guest:guest@rabbitmq:5672/"
    )

    try:
        params = pika.URLParameters(rabbitmq_url)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()

        channel.queue_declare(
            queue="sentiment_analysis",
            durable=True
        )

        message = json.dumps({
            "post_id": post_id,
            "text": text
        })

        channel.basic_publish(
            exchange="",
            routing_key="sentiment_analysis",
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2  # persist message
            )
        )

        connection.close()
        logging.info(f"Sentiment analysis event published for post {post_id}")

    except Exception as e:
        logging.warning(
            f"[messaging] RabbitMQ unavailable, skipping sentiment analysis event: {e}"
        )


def publish_text_generation_event(post_id: int, text: str) -> None:
    """
    Publish text generation event.
    
    Args:
        post_id: ID of the post to generate text for
        text: Original text to base generation on
    
    IMPORTANT:
    - This must NEVER break the REST API.
    - If RabbitMQ is unavailable, we silently skip.
    """
    rabbitmq_url = os.getenv(
        "RABBITMQ_URL",
        "amqp://guest:guest@rabbitmq:5672/"
    )

    try:
        params = pika.URLParameters(rabbitmq_url)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()

        channel.queue_declare(
            queue="text_generation",
            durable=True
        )

        message = json.dumps({
            "post_id": post_id,
            "text": text
        })

        channel.basic_publish(
            exchange="",
            routing_key="text_generation",
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2  # persist message
            )
        )

        connection.close()
        logging.info(f"Text generation event published for post {post_id}")

    except Exception as e:
        logging.warning(
            f"[messaging] RabbitMQ unavailable, skipping text generation event: {e}"
        )