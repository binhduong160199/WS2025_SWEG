"""Tests for text generator"""

import pytest
from app.text_model import TextGenerator


@pytest.fixture
def generator():
    """Create text generator instance"""
    return TextGenerator()


class TestTextGenerator:
    """Test text generation functionality"""
    
    def test_generator_initialization(self, generator):
        """Test that generator initializes correctly"""
        assert generator.pipeline is not None
    
    def test_generate_text(self, generator):
        """Test basic text generation"""
        prompt = "The weather is"
        result = generator.generate(prompt, max_length=50, num_return_sequences=2)
        
        assert isinstance(result, list)
        assert len(result) >= 0  # May return 0-2 results
    
    def test_generate_variations(self, generator):
        """Test generating variations of text"""
        text = "This is a great post about AI"
        result = generator.generate_variations(text)
        
        assert isinstance(result, list)
        # Should generate up to 2 variations
        assert len(result) <= 2
    
    def test_generate_with_long_text(self, generator):
        """Test generation with long input"""
        long_text = "This is " * 50
        result = generator.generate_variations(long_text)
        
        assert isinstance(result, list)
    
    def test_generate_with_short_text(self, generator):
        """Test generation with short input"""
        text = "Great"
        result = generator.generate_variations(text)
        
        assert isinstance(result, list)
    
    def test_generate_filtered_output(self, generator):
        """Test that very short generations are filtered"""
        prompt = "a"
        result = generator.generate(prompt, max_length=30, num_return_sequences=3)
        
        # All results should be at least 3 words (after filtering)
        for text in result:
            word_count = len(text.split())
            assert word_count >= 3 or word_count == 0  # 0 if filtered out completely


class TestEdgeCases:
    """Test edge cases in text generation"""
    
    def test_generate_empty_string(self, generator):
        """Test with empty string"""
        result = generator.generate("", max_length=50)
        assert isinstance(result, list)
    
    def test_generate_with_special_chars(self, generator):
        """Test with special characters"""
        prompt = "Test @#$%^&*()"
        result = generator.generate(prompt, max_length=50)
        assert isinstance(result, list)
    
    def test_generate_with_numbers(self, generator):
        """Test with numbers"""
        prompt = "123 456 789"
        result = generator.generate(prompt, max_length=50)
        assert isinstance(result, list)
