import pytest
from app.analyzer import analyze_sentiment


def test_positive_sentiment():
    """Test positive sentiment detection"""
    text = "This is absolutely wonderful and amazing!"
    label, score = analyze_sentiment(text)
    
    assert label == "POSITIVE"
    assert float(score) > 0.9


def test_negative_sentiment():
    """Test negative sentiment detection"""
    text = "This is terrible and awful, I hate it!"
    label, score = analyze_sentiment(text)
    
    assert label == "NEGATIVE"
    assert float(score) > 0.9


def test_truncate_long_text():
    """Test that long text is handled properly"""
    text = "Great! " * 200  # Very long text
    label, score = analyze_sentiment(text)
    
    assert label in ["POSITIVE", "NEGATIVE"]
    assert 0.0 <= float(score) <= 1.0
