import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# OpenAI API configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_ORG_ID = os.getenv("OPENAI_ORG_ID", "")  # Optional

# Model parameters
DEFAULT_MODEL = "gpt-3.5-turbo"
MAX_TOKENS = 500
TEMPERATURE = 0.7

# Rate Limiting
MAX_REQUESTS_PER_MINUTE = 10  # Adjust based on your API tier

# System prompts
FINANCIAL_ASSISTANT_PROMPT = """
You are a helpful financial assistant for SmartSaverSG, a bank interest rate calculator.
Your role is to help users understand their bank interest calculations and provide 
financial advice based on their specific situation.

When responding to users:
1. Be concise and clear in your explanations
2. Format financial figures with $ and commas (e.g., $1,000.00)
3. Focus on factual information about banking products
4. Avoid making specific investment recommendations
5. Clarify that you're providing general information, not financial advice
"""