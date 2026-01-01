import json
import os
import time
import pika
import logging

from app.db import get_post_text, update_sentiment
from app.analyzer import analyze_sentiment

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

QUEUE_NAME = "sentiment_analysis"


def _connect_with_retry():
    """Connect to RabbitMQ with retry logic"""
    rabbitmq_url = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672/")
    params = pika.URLParameters(rabbitmq_url)

    while True:
        try:
            return pika.BlockingConnection(params)
        except Exception as e:
            logging.info(f"[sentiment] RabbitMQ not ready yet: {e}. Retrying in 2s...")
            time.sleep(2)


def handle_message(ch, method, properties, body):
    """Handle incoming sentiment analysis request"""
    try:
        data = json.loads(body.decode("utf-8"))
        post_id = int(data["post_id"])
    except Exception as e:
        logging.error(f"[sentiment] Invalid message: {body!r} error={e}")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return

    try:
        # Get post text from database
        text = get_post_text(post_id)
        if text is None:
            logging.warning(f"[sentiment] No text found for post_id={post_id}")
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return

        # Analyze sentiment
        logging.info(f"[sentiment] Analyzing post_id={post_id}")
        label, score = analyze_sentiment(text)
        
        # Update database
        update_sentiment(post_id, label, score)

        logging.info(f"[sentiment] post_id={post_id} -> {label} (score={score})")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        logging.error(f"[sentiment] Failed processing post_id={post_id}: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)


def main():
    """Main consumer loop"""
    logging.info("[sentiment] Starting sentiment analysis service...")
    
    conn = _connect_with_retry()
    ch = conn.channel()

    ch.queue_declare(queue=QUEUE_NAME, durable=True)
    ch.basic_qos(prefetch_count=1)
    ch.basic_consume(queue=QUEUE_NAME, on_message_callback=handle_message)

    logging.info("[sentiment] Listening for sentiment analysis jobs...")
    ch.start_consuming()


if __name__ == "__main__":
    main()
