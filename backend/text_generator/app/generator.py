from transformers import pipeline
import logging

# Global variable to cache the model
_generator_pipeline = None

def get_generator_pipeline():
    """Get or create text generation pipeline (with caching)"""
    global _generator_pipeline
    if _generator_pipeline is None:
        logging.info("[text-gen] Loading GPT-2 model...")
        _generator_pipeline = pipeline(
            "text-generation",
            model="gpt2",  # smallest version
            device=-1      # Use CPU
        )
        logging.info("[text-gen] Model loaded successfully")
    return _generator_pipeline

def generate_text(prompt: str, max_length: int = 50) -> str:
    try:
        pipeline_obj = get_generator_pipeline()
        # Optional: truncate prompt if too long (for safety)
        max_prompt_chars = 200
        if len(prompt) > max_prompt_chars:
            prompt = prompt[:max_prompt_chars]
        result = pipeline_obj(prompt, max_length=max_length, num_return_sequences=1)
        logging.info(f"[text-gen] Generation result: {result}")
        generated_full = result[0]['generated_text']
        if generated_full.startswith(prompt):
            generated = generated_full[len(prompt):].strip()
        else:
            generated = generated_full
        return generated
    except Exception as e:
        import traceback
        logging.error(f"[text-gen] Error generating text: {e}\n{traceback.format_exc()}")
        return "[generation failed]"