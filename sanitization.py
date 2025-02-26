import re
import html

def sanitize_user_input(input_text):
    """
    Sanitize user input to prevent prompt injection and other issues
    """
    if not input_text:
        return ""
    
    # Convert to string if not already
    input_text = str(input_text)
    
    # Escape HTML entities
    sanitized = html.escape(input_text)
    
    # Remove any potential prompt injection attempts
    sanitized = re.sub(r'(system:|assistant:|user:)', '', sanitized, flags=re.IGNORECASE)
    
    # Limit length
    max_length = 500
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length] + "..."
    
    return sanitized.strip()

def sanitize_ai_output(output_text):
    """
    Sanitize AI output to ensure safe formatting and consistent style
    """
    if not output_text:
        return "I'm sorry, I couldn't generate a response."
    
    # Convert to string if not already
    output_text = str(output_text)
    
    # Format financial figures consistently
    # Find patterns like $X, $X.Y, $X.YZ and add commas for thousands
    def add_commas(match):
        num_str = match.group(1)
        try:
            if '.' in num_str:
                whole, decimal = num_str.split('.')
                whole_with_commas = f"{int(whole):,}"
                return f"${whole_with_commas}.{decimal}"
            else:
                return f"${int(num_str):,}"
        except ValueError:
            return match.group(0)
    
    output_text = re.sub(r'\$(\d+(?:\.\d+)?)', add_commas, output_text)
    
    # Ensure proper formatting of percentages
    output_text = re.sub(r'(\d+(?:\.\d+)?)%', r'\1%', output_text)
    
    # Remove any potential unsafe HTML
    output_text = html.escape(output_text)
    
    # Convert escaped HTML back to safe markdown
    output_text = output_text.replace('&lt;b&gt;', '**').replace('&lt;/b&gt;', '**')
    output_text = output_text.replace('&lt;i&gt;', '*').replace('&lt;/i&gt;', '*')
    
    return output_text