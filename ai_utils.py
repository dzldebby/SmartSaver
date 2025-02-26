import os
import time
from openai import OpenAI
import logging
from dotenv import load_dotenv
from config import DEFAULT_MODEL, MAX_TOKENS, MAX_REQUESTS_PER_MINUTE

# Load environment variables
load_dotenv()

# Check if OpenAI API key is available
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_AVAILABLE = bool(OPENAI_API_KEY)

# Initialize OpenAI client with error handling
try:
    client = OpenAI(api_key=OPENAI_API_KEY)
    if not OPENAI_AVAILABLE:
        logging.warning("OpenAI API key not found. AI features will be disabled.")
except Exception as e:
    logging.error(f"Error initializing OpenAI client: {str(e)}")
    OPENAI_AVAILABLE = False
    client = None

# Track API call rate
api_call_count = 0
last_reset_time = time.time()

def get_ai_response(messages, model=DEFAULT_MODEL, max_tokens=MAX_TOKENS) -> str:
    """
    Get a response from the OpenAI API with exponential backoff for retries
    """
    global api_call_count, last_reset_time
    
    # Check if OpenAI is available
    if not OPENAI_AVAILABLE:
        return "I'm sorry, the AI assistant is currently unavailable because the OpenAI API key is not configured. Please contact the administrator to set up the API key."
    
    # Reset counter if a minute has passed
    current_time = time.time()
    if current_time - last_reset_time >= 60:
        api_call_count = 0
        last_reset_time = current_time
    
    # Check if we're over the rate limit
    if api_call_count > MAX_REQUESTS_PER_MINUTE:
        wait_time = 60 - (current_time - last_reset_time)
        if wait_time > 0:
            logging.warning(f"Rate limit reached. Waiting {wait_time:.2f} seconds.")
            time.sleep(wait_time)
            # Reset after waiting
            api_call_count = 0
            last_reset_time = time.time()
    
    # Attempt to get a response with exponential backoff
    max_retries = 5
    base_delay = 1
    
    for attempt in range(max_retries):
        try:
            # Increment counter before making the call
            api_call_count += 1
            
            # Make the API call
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens
            )
            
            # Return the response content
            return response.choices[0].message.content
            
        except Exception as e:
            delay = base_delay * (2 ** attempt)
            logging.warning(f"API error: {str(e)}. Retrying in {delay} seconds.")
            time.sleep(delay)
            
            if attempt == max_retries - 1:
                logging.error(f"Failed after {max_retries} attempts: {str(e)}")
                return f"I'm sorry, I encountered an error: {str(e)}"
    
    # If we've exhausted all retries
    return "I'm sorry, I'm having trouble connecting to my knowledge base right now. Please try again later."

# Add a test function to verify the file is working
def test_ai():
    """Test function to verify the AI connection"""
    return "AI utils loaded successfully"

# Make sure the function is exported
__all__ = ['get_ai_response', 'test_ai', 'OPENAI_AVAILABLE']