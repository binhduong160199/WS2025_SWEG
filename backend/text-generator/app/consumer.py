import json
import os
import time
import pika
import logging

from app.db import get_post_text, save_generated_text
from app.generator import generate_text

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

QUEUE_NAME = "text_generation"


def _connect_with_retry():
    """Connect to RabbitMQ with retry logic"""
    rabbitmq_url = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672/")
    params = pika.URLParameters(rabbitmq_url)

    while True:
        try:
            return pika.BlockingConnection(params)
        except Exception as e:
            logging.info(f"[text-gen] RabbitMQ not ready yet: {e}. Retrying in 2s...")
            time.sleep(2)


def handle_message(ch, method, properties, body):
    """Handle incoming text generation request"""
    try:
        data = json.loads(body.decode("utf-8"))
        post_id = int(data["post_id"])
        logging.info(f"[text-gen] Received request for post_id={post_id}")
    except Exception as e:
        logging.error(f"[text-gen] Invalid message: {body!r} error={e}")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return

    try:
        # Get post text from database
        text = get_post_text(post_id)
        if text is None:
            logging.warning(f"[text-gen] No text found for post_id={post_id}")
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return

        # Generate text continuation
        logging.info(f"[text-gen] Generating for post_id={post_id}, text_length={len(text)}")
        generated = generate_text(text, max_length=100)
        
        # Save to database
        logging.info(f"[text-gen] Saving generated text for post_id={post_id}")
        save_generated_text(post_id, generated)

        logging.info(f"[text-gen] SUCCESS - Generated for post_id={post_id} (length={len(generated)})")
        logging.info(f"[text-gen] SUCCESS - Generated for post_id={post_id} (txt={generated})")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        logging.error(f"[text-gen] FAILED processing post_id={post_id}: {e}", exc_info=True)
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)  # Don't requeue on error


def main():
    """Main consumer loop"""
    logging.info("[text-gen] Starting text generation service...")
    
    # Preload the model to avoid delays on first request
    logging.info("[text-gen] Preloading GPT-2 model...")
    try:
        generate_text("Test warm-up", max_length=20)
        logging.info("[text-gen] Model preloaded successfully")
    except Exception as e:
        logging.warning(f"[text-gen] Failed to preload model: {e}")
    
    conn = _connect_with_retry()
    ch = conn.channel()

    ch.queue_declare(queue=QUEUE_NAME, durable=True)
    ch.basic_qos(prefetch_count=1)
    ch.basic_consume(queue=QUEUE_NAME, on_message_callback=handle_message)

    logging.info("[text-gen] Listening for text generation jobs...")
    ch.start_consuming()


if __name__ == "__main__":
    main()
