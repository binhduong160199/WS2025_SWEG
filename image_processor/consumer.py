#!/usr/bin/env python3
"""Image processor microservice: consumes resize tasks from RabbitMQ,
fetches full image from backend, resizes it, and PATCHes thumbnail back.
"""
import os
import time
import json
import base64
import logging
from io import BytesIO

import requests
from PIL import Image
import pika

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('image_processor')


BACKEND_URL = os.environ.get('BACKEND_URL', 'http://backend:5001/api')
RABBITMQ_URL = os.environ.get('RABBITMQ_URL', 'amqp://guest:guest@rabbitmq:5672/')
QUEUE_NAME = os.environ.get('QUEUE_NAME', 'image_resize')


def process_message(body: bytes) -> bool:
    try:
        data = json.loads(body)
        post_id = int(data.get('post_id'))
    except Exception as e:
        logger.exception('Invalid message payload')
        return True

    logger.info('Processing post_id=%s', post_id)

    # Fetch post detail from backend
    try:
        resp = requests.get(f"{BACKEND_URL}/posts/{post_id}", timeout=10)
        if resp.status_code != 200:
            logger.error('Failed to fetch post %s: status=%s', post_id, resp.status_code)
            return True
        post = resp.json()
    except Exception:
        logger.exception('Error fetching post from backend')
        return False

    image_b64 = post.get('image')
    if not image_b64:
        logger.info('No image found for post %s, skipping', post_id)
        return True

    try:
        image_bytes = base64.b64decode(image_b64)
        img = Image.open(BytesIO(image_bytes))
        img = img.convert('RGB')
        max_size = (200, 200)
        img.thumbnail(max_size, Image.LANCZOS)

        out = BytesIO()
        img.save(out, format='JPEG', quality=85)
        thumb_bytes = out.getvalue()
        thumb_b64 = base64.b64encode(thumb_bytes).decode('utf-8')
    except Exception:
        logger.exception('Failed to resize image for post %s', post_id)
        return False

    # PATCH thumbnail back to backend
    try:
        patch_resp = requests.patch(
            f"{BACKEND_URL}/posts/{post_id}/thumbnail",
            json={'thumbnail': thumb_b64},
            timeout=10
        )
        if patch_resp.status_code not in (200, 201):
            logger.error('Backend returned %s when updating thumbnail for %s', patch_resp.status_code, post_id)
            return False
    except Exception:
        logger.exception('Failed to PATCH thumbnail to backend')
        return False

    logger.info('Thumbnail updated for post %s', post_id)
    return True


def main():
    params = pika.URLParameters(RABBITMQ_URL)
    while True:
        try:
            connection = pika.BlockingConnection(params)
            channel = connection.channel()
            channel.queue_declare(queue=QUEUE_NAME, durable=True)
            channel.basic_qos(prefetch_count=1)

            def callback(ch, method, properties, body):
                logger.info('Received message: %s', body)
                success = process_message(body)
                if success:
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                else:
                    # On failure, ack to avoid endless loops; in production consider dead-lettering
                    ch.basic_ack(delivery_tag=method.delivery_tag)

            channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback)
            logger.info('Waiting for messages. To exit press CTRL+C')
            channel.start_consuming()

        except pika.exceptions.AMQPConnectionError:
            logger.exception('Cannot connect to RabbitMQ, retrying in 5s...')
            time.sleep(5)
        except KeyboardInterrupt:
            try:
                connection.close()
            except Exception:
                pass
            break


if __name__ == '__main__':
    main()
