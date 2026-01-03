import pytest
from app.generator import generate_text


def test_text_generation():
    """Test that text generation works"""
    prompt = "Once upon a time"
    generated = generate_text(prompt, max_length=30)
    
    # Check that we got text back
    assert len(generated) > len(prompt)
    assert generated.startswith(prompt)


def test_short_prompt():
    """Test generation with short prompt"""
    prompt = "Hello"
    generated = generate_text(prompt, max_length=20)
    
    assert len(generated) > len(prompt)


def test_long_prompt():
    """Test that long prompts are handled"""
    prompt = "This is a very long prompt. " * 50
    generated = generate_text(prompt, max_length=50)
    
    # Should still generate something
    assert len(generated) > 0
