"""Text Generation Model using GPT2"""

from transformers import pipeline
import logging

logger = logging.getLogger(__name__)

class TextGenerator:
    def __init__(self):
        """Initialize GPT2 text generation pipeline"""
        try:
            # Use the high-level `pipeline` helper which accepts model ids (strings)
            # and handles tokenizer/model loading internally.
            # `device=-1` forces CPU. Change to `device=0` to use GPU if available.
            self.pipeline = pipeline(
                "text-generation",
                model="gpt2",
                device=-1,
            )
            logger.info("Text generator initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize text generator: {e}")
            raise
    
    def generate(self, prompt: str, max_length: int = 100, num_return_sequences: int = 3) -> list:
        """
        Generate text based on prompt
        
        Args:
            prompt: Starting text for generation
            max_length: Maximum length of generated text
            num_return_sequences: Number of variations to generate
            
        Returns:
            list of generated text strings
        """
        try:
            # Limit prompt to reasonable size
            prompt = prompt[:200]
            
            results = self.pipeline(
                prompt,
                max_length=max_length,
                num_return_sequences=num_return_sequences,
                temperature=0.7,  # Control randomness
                top_p=0.95,       # Nucleus sampling
                do_sample=True,
                repetition_penalty=2.0
            )
            
            # Extract text from results
            generated_texts = [r['generated_text'].replace(prompt, '').strip() for r in results]
            
            # Filter out empty or too-short generations
            generated_texts = [t for t in generated_texts if len(t.split()) > 3]
            
            return generated_texts
        
        except Exception as e:
            logger.error(f"Error generating text: {e}")
            return []
    
    def generate_variations(self, text: str) -> list:
        """
        Generate variations/suggestions for post text
        
        Args:
            text: Original post text
            
        Returns:
            list of suggested variations
        """
        try:
            # Use last few words as prompt
            words = text.split()
            prompt = ' '.join(words[-3:]) if len(words) >= 3 else text
            
            generated = self.generate(prompt, max_length=80, num_return_sequences=2)
            
            return generated
        
        except Exception as e:
            logger.error(f"Error generating variations: {e}")
            return []
