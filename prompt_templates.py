from config import FINANCIAL_ASSISTANT_PROMPT

# System prompts dictionary
SYSTEM_PROMPTS = {
    "financial_assistant": FINANCIAL_ASSISTANT_PROMPT
}

def create_user_prompt(user_data, question):
    """
    Create a formatted prompt with user context and question
    """
    context = f"""
Based on the following user information:
- Savings amount: ${user_data.get('savings_amount', 0):,.2f}
- Has salary credited: {'Yes' if user_data.get('has_salary', False) else 'No'}
"""
    
    if user_data.get('has_salary', False):
        context += f"- Salary amount: ${user_data.get('salary_amount', 0):,.2f}\n"
    
    context += f"""- Card spend: ${user_data.get('spend_amount', 0):,.2f}
- Bill payments: {user_data.get('giro_count', 0)}
- Has insurance: {'Yes' if user_data.get('has_insurance', False) else 'No'}
- Has investments: {'Yes' if user_data.get('has_investments', False) else 'No'}
"""
    
    return f"{context}\n\nUser question: {question}"

def generate_suggestions(bank_results):
    """
    Generate contextual suggestions based on calculation results
    """
    if not bank_results:
        return ["What are the best banks for savings?", 
                "How can I maximize my interest?", 
                "What requirements do banks have?"]
    
    # Sort banks by interest rate
    sorted_banks = sorted(bank_results, key=lambda x: x['annual_interest'], reverse=True)
    top_bank = sorted_banks[0]['bank']
    
    suggestions = [
        f"Why is {top_bank} giving me the highest interest?",
        "How can I increase my interest rate?",
        "What if I increase my savings amount?",
        "Which bank has the easiest requirements?"
    ]
    
    # Add bank-specific suggestions
    if top_bank == "UOB One":
        suggestions.append("What are the requirements for UOB One?")
    elif top_bank == "OCBC 360":
        suggestions.append("How does OCBC 360 calculate interest?")
    elif top_bank == "SC BonusSaver":
        suggestions.append("What bonus categories does SC BonusSaver have?")
    
    return suggestions[:4]  # Limit to 4 suggestions