"""RabbitMQ Consumer for Sentiment Analysis"""

import pika
import json
import logging
import os
import time
from app.sentiment_model import SentimentAnalyzer
from app.db import DatabaseConnection

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SentimentConsumer:
    def __init__(self):
        """Initialize sentiment analysis consumer"""
        self.rabbitmq_url = os.getenv('RABBITMQ_URL', 'amqp://guest:guest@rabbitmq:5672/')
        self.analyzer = SentimentAnalyzer()
        self.db = DatabaseConnection()
        
        logger.info("SentimentConsumer initialized")
    
    def connect(self) -> pika.BlockingConnection:
        """Connect to RabbitMQ with retries"""
        retries = 0
        max_retries = 30
        
        while retries < max_retries:
            try:
                connection = pika.BlockingConnection(
                    pika.URLParameters(self.rabbitmq_url)
                )
                logger.info("Connected to RabbitMQ")
                return connection
            except Exception as e:
                retries += 1
                logger.warning(f"RabbitMQ connection attempt {retries}/{max_retries} failed: {e}")
                time.sleep(2)
        
        raise Exception("Failed to connect to RabbitMQ after retries")
    
    def callback(self, ch, method, properties, body):
        """Process sentiment analysis message"""
        try:
            message = json.loads(body)
            post_id = message.get('post_id')
            text = message.get('text')
            
            logger.info(f"Processing sentiment for post {post_id}")
            
            # Mark as processing
            self.db.set_processing_status(post_id, 'processing')
            
            # Analyze sentiment
            result = self.analyzer.analyze(text)
            
            # Update database
            self.db.update_sentiment(
                post_id,
                result['label'],
                result['score']
            )
            
            logger.info(f"Sentiment analysis completed for post {post_id}: {result}")
            
            # Acknowledge message
            ch.basic_ack(delivery_tag=method.delivery_tag)
            
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            # Negative acknowledge to requeue
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
    
    def start(self):
        """Start consuming messages"""
        connection = self.connect()
        channel = connection.channel()
        
        # Declare queue
        queue_name = 'sentiment_analysis'
        channel.queue_declare(queue=queue_name, durable=True)
        
        # Set up consumer
        channel.basic_qos(prefetch_count=1)  # One message at a time
        channel.basic_consume(
            queue=queue_name,
            on_message_callback=self.callback
        )
        
        logger.info(f"Starting to listen on queue '{queue_name}'")
        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            logger.info("Shutting down...")
            channel.stop_consuming()
            connection.close()

if __name__ == '__main__':
    consumer = SentimentConsumer()
    consumer.start()
