"""Sentiment Analysis Model"""

from transformers import pipeline
import logging

logger = logging.getLogger(__name__)

class SentimentAnalyzer:
    def __init__(self):
        """Initialize sentiment analysis pipeline"""
        try:
            # Use distilbert for faster inference
            self.pipeline = pipeline(
                "sentiment-analysis",
                model="distilbert-base-uncased-finetuned-sst-2-english",
                device=-1  # Use CPU (-1), or device=0 for GPU if available
            )
            logger.info("Sentiment analyzer initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize sentiment analyzer: {e}")
            raise

    def analyze(self, text: str) -> dict:
        """
        Analyze sentiment of given text
        
        Args:
            text: Text to analyze
            
        Returns:
            dict with keys:
                - label: 'POSITIVE' or 'NEGATIVE'
                - score: float between 0 and 1
        """
        try:
            result = self.pipeline(text[:512])  # Truncate to 512 chars (model limit)
            
            return {
                'label': result[0]['label'],
                'score': result[0]['score']
            }
        except Exception as e:
            logger.error(f"Error analyzing sentiment: {e}")
            return {
                'label': 'UNKNOWN',
                'score': 0.0
            }
