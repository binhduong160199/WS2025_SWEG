"""Tests for sentiment analyzer"""

import pytest
from app.sentiment_model import SentimentAnalyzer


@pytest.fixture
def analyzer():
    """Create sentiment analyzer instance"""
    return SentimentAnalyzer()


class TestSentimentAnalyzer:
    """Test sentiment analysis functionality"""
    
    def test_analyzer_initialization(self, analyzer):
        """Test that analyzer initializes correctly"""
        assert analyzer.pipeline is not None
    
    def test_analyze_positive_sentiment(self, analyzer):
        """Test analyzing positive sentiment text"""
        result = analyzer.analyze("I love this! It's amazing!")
        
        assert 'label' in result
        assert 'score' in result
        assert result['label'] in ['POSITIVE', 'NEGATIVE']
        assert 0.0 <= result['score'] <= 1.0
    
    def test_analyze_negative_sentiment(self, analyzer):
        """Test analyzing negative sentiment text"""
        result = analyzer.analyze("This is terrible and awful")
        
        assert 'label' in result
        assert 'score' in result
        assert result['label'] in ['POSITIVE', 'NEGATIVE']
        assert 0.0 <= result['score'] <= 1.0
    
    def test_analyze_long_text(self, analyzer):
        """Test analyzing text longer than model limit"""
        long_text = "Great " * 200  # This will exceed 512 characters
        result = analyzer.analyze(long_text)
        
        assert 'label' in result
        assert 'score' in result
        # Should handle long text gracefully
        assert result['label'] in ['POSITIVE', 'NEGATIVE', 'UNKNOWN']
    
    def test_analyze_empty_text(self, analyzer):
        """Test analyzing empty text"""
        result = analyzer.analyze("")
        
        assert 'label' in result
        assert 'score' in result
    
    def test_analyze_neutral_text(self, analyzer):
        """Test analyzing neutral text"""
        result = analyzer.analyze("The sky is blue")
        
        assert 'label' in result
        assert 'score' in result
        assert result['label'] in ['POSITIVE', 'NEGATIVE']
