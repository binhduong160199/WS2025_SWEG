import json
import os
import time
import pika
import logging

from app.db import save_generated_text, init_text_suggestions_table
from app.generator import generate_text


def wait_for_db_and_init_table(max_retries=30, delay=2):
    for i in range(max_retries):
        try:
            init_text_suggestions_table()
            logging.info("[text-gen] text_suggestions table ready")
            return
        except Exception as e:
            logging.warning(f"[text-gen] Waiting for DB ({i+1}/{max_retries}): {e}")
            time.sleep(delay)
    raise RuntimeError("Failed to connect to DB after retries")

# --------------------------------------------------
# Logging
# --------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

QUEUE_NAME = "text_generation"


def _connect_with_retry():
    """Connect to RabbitMQ with retry logic"""
    rabbitmq_url = os.getenv(
        "RABBITMQ_URL",
        "amqp://guest:guest@rabbitmq:5672/"
    )
    params = pika.URLParameters(rabbitmq_url)

    while True:
        try:
            return pika.BlockingConnection(params)
        except Exception as e:
            logging.info(
                f"[text-gen] RabbitMQ not ready yet: {e}. Retrying in 2s..."
            )
            time.sleep(2)


def handle_message(ch, method, properties, body):
    """Handle incoming text generation request"""
    try:
        data = json.loads(body.decode("utf-8"))
        prompt = data.get("prompt", "").strip()

        if not prompt:
            raise ValueError("Missing prompt")

        logging.info(f"[text-gen] Received generation request (length={len(prompt)})")

    except Exception as e:
        logging.error(f"[text-gen] Invalid message: {body!r} error={e}")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return

    try:
        # Generate text
        logging.info("[text-gen] Generating text...")
        generated = generate_text(prompt, max_length=100)

        # Save result (KHÔNG CẦN post_id)
        logging.info("[text-gen] Saving generated text")
        save_generated_text(generated)

        logging.info(f"[text-gen] SUCCESS (length={len(generated)})")

        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        logging.error(f"[text-gen] FAILED processing message: {e}", exc_info=True)
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)


def main():
    """Main consumer loop"""
    logging.info("[text-gen] Starting text generation service...")

    # WAIT for DB instead of failing immediately
    wait_for_db_and_init_table()

    # Warm-up model
    try:
        logging.info("[text-gen] Preloading GPT-2 model...")
        generate_text("Warm-up", max_length=20)
        logging.info("[text-gen] Model preloaded successfully")
    except Exception as e:
        logging.warning(f"[text-gen] Model preload failed: {e}")

    # RabbitMQ connection (already has retry)
    conn = _connect_with_retry()
    ch = conn.channel()

    ch.queue_declare(queue=QUEUE_NAME, durable=True)
    ch.basic_qos(prefetch_count=1)
    ch.basic_consume(
        queue=QUEUE_NAME,
        on_message_callback=handle_message
    )

    logging.info("[text-gen] Waiting for text generation jobs...")
    ch.start_consuming()

if __name__ == "__main__":
    main()