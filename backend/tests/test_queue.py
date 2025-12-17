import unittest
import json
import base64
from unittest.mock import patch, MagicMock

from app import create_app


class TestImageQueue(unittest.TestCase):
    def setUp(self):
        # use in-memory sqlite for fast tests
        self.app = create_app({'TESTING': True, 'DATABASE': ':memory:'})
        self.client = self.app.test_client()

    @patch('app.routes.pika.BlockingConnection')
    def test_post_with_image_publishes_message(self, mock_blocking_conn):
        mock_channel = MagicMock()
        mock_conn = MagicMock()
        mock_conn.channel.return_value = mock_channel
        mock_blocking_conn.return_value = mock_conn

        image_b64 = base64.b64encode(b'test-image-bytes').decode('utf-8')
        resp = self.client.post(
            '/api/posts',
            data=json.dumps({'user': 'tester', 'text': 'hello', 'image': image_b64}),
            content_type='application/json'
        )

        self.assertEqual(resp.status_code, 201)
        # ensure we attempted to connect to RabbitMQ and publish
        mock_blocking_conn.assert_called()
        mock_channel.queue_declare.assert_called_with(queue='image_resize', durable=True)
        mock_channel.basic_publish.assert_called()


if __name__ == '__main__':
    unittest.main()
