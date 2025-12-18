import json
import os
import time
import pika

from app.db import get_full_image, update_thumbnail
from app.resize import make_thumbnail


QUEUE_NAME = "image_resize"


def _connect_with_retry():
    rabbitmq_url = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672/")
    params = pika.URLParameters(rabbitmq_url)

    # Simple retry loop so container can start even if rabbitmq isn't ready yet
    while True:
        try:
            return pika.BlockingConnection(params)
        except Exception as e:
            print(f"[resizer] RabbitMQ not ready yet: {e}. Retrying in 2s...")
            time.sleep(2)


def handle_message(ch, method, properties, body):
    try:
        data = json.loads(body.decode("utf-8"))
        post_id = int(data["post_id"])
    except Exception as e:
        print(f"[resizer] Invalid message: {body!r} error={e}")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return

    try:
        full = get_full_image(post_id)
        if full is None:
            print(f"[resizer] No full image found for post_id={post_id}")
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return

        thumb = make_thumbnail(full, max_width=600, quality=70)
        update_thumbnail(post_id, thumb)

        print(f"[resizer] Thumbnail created for post_id={post_id} (size={len(thumb)} bytes)")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        # If something failed, don't ack -> message can be retried
        print(f"[resizer] Failed processing post_id={post_id}: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)


def main():
    conn = _connect_with_retry()
    ch = conn.channel()

    ch.queue_declare(queue=QUEUE_NAME, durable=True)
    ch.basic_qos(prefetch_count=1)
    ch.basic_consume(queue=QUEUE_NAME, on_message_callback=handle_message)

    print("[resizer] Listening for image resize jobs...")
    ch.start_consuming()


if __name__ == "__main__":
    main()