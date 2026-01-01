from transformers import pipeline
import logging

# Global variable to cache the model
_generator_pipeline = None


def get_generator_pipeline():
    """Get or create text generation pipeline (with caching)"""
    global _generator_pipeline
    
    if _generator_pipeline is None:
        logging.info("[text-gen] Loading GPT-2 model...")
        # Use the smallest GPT-2 model for fast loading
        _generator_pipeline = pipeline(
            "text-generation",
            model="gpt2",  # smallest version
            device=-1  # Use CPU
        )
        logging.info("[text-gen] Model loaded successfully")
    
    return _generator_pipeline


def generate_text(prompt: str, max_length: int = 50) -> str:
    """
    Generate text continuation using GPT-2
    
    Args:
        prompt: Text to continue from
        max_length: Maximum total length (prompt + generation)
        
    Returns:
        str: Generated text
    """
    try:
        pipeline_obj = get_generator_pipeline()
        
        # Truncate prompt if too long
        max_prompt_chars = 200
        if len(prompt) > max_prompt_chars:
            prompt = prompt[:max_prompt_chars]
        
        # Generate text
        result = pipeline_obj(
            prompt,
            max_length=max_length,
            num_return_sequences=1,
            temperature=0.7,
            top_p=0.9,
            do_sample=True,
            pad_token_id=50256  # GPT-2 EOS token
        )[0]
        
        generated = result['generated_text']
        
        return generated
        
    except Exception as e:
        logging.error(f"[text-gen] Error generating text: {e}")
        return f"{prompt}... [generation failed]"
