from transformers import pipeline
import logging

# Global variable to cache the model
_sentiment_pipeline = None


def get_sentiment_pipeline():
    """Get or create sentiment analysis pipeline (with caching)"""
    global _sentiment_pipeline
    
    if _sentiment_pipeline is None:
        logging.info("[sentiment] Loading sentiment analysis model...")
        # Use a small, fast model
        _sentiment_pipeline = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english",
            device=-1  # Use CPU
        )
        logging.info("[sentiment] Model loaded successfully")
    
    return _sentiment_pipeline


def analyze_sentiment(text: str) -> tuple[str, str]:
    """
    Analyze sentiment of text
    
    Returns:
        tuple: (sentiment_label, sentiment_score_str)
        Example: ("POSITIVE", "0.9998")
    """
    try:
        pipeline_obj = get_sentiment_pipeline()
        
        # Truncate text if too long (model has max token limit)
        max_chars = 500
        if len(text) > max_chars:
            text = text[:max_chars]
        
        result = pipeline_obj(text)[0]
        
        label = result['label']  # "POSITIVE" or "NEGATIVE"
        score = result['score']  # confidence 0.0 to 1.0
        
        # Format score as string with 4 decimal places
        score_str = f"{score:.4f}"
        
        return label, score_str
        
    except Exception as e:
        logging.error(f"[sentiment] Error analyzing sentiment: {e}")
        return "UNKNOWN", "0.0000"
