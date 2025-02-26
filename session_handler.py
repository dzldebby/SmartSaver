import streamlit as st
import time
from config import FINANCIAL_ASSISTANT_PROMPT

def initialize_chat_session():
    """
    Initialize the chat session in Streamlit's session state
    """
    if 'chat_messages' not in st.session_state:
        st.session_state.chat_messages = []
    
    if 'chat_context' not in st.session_state:
        st.session_state.chat_context = {
            'user_data': {},
            'calculation_results': [],
            'last_updated': time.time()
        }

def update_chat_with_calculation(bank_results, user_data):
    """
    Update the chat context with new calculation results
    """
    initialize_chat_session()
    
    # Update context with new data
    st.session_state.chat_context['user_data'] = user_data
    st.session_state.chat_context['calculation_results'] = bank_results
    st.session_state.chat_context['last_updated'] = time.time()
    
    # Clear previous messages when new calculation is performed
    st.session_state.chat_messages = []

def add_user_message(message):
    """
    Add a user message to the chat history
    """
    initialize_chat_session()
    
    st.session_state.chat_messages.append({
        "role": "user",
        "content": message
    })

def add_assistant_message(message):
    """
    Add an assistant message to the chat history
    """
    initialize_chat_session()
    
    st.session_state.chat_messages.append({
        "role": "assistant",
        "content": message
    })

def get_api_messages():
    """
    Get formatted messages for the OpenAI API
    """
    initialize_chat_session()
    
    # Start with system message
    messages = [
        {"role": "system", "content": FINANCIAL_ASSISTANT_PROMPT}
    ]
    
    # Add context about the user's data and calculation results
    context = _format_context_message()
    if context:
        messages.append({"role": "system", "content": context})
    
    # Add conversation history
    messages.extend(st.session_state.chat_messages)
    
    return messages

def get_chat_messages():
    """
    Get the chat messages for display
    """
    initialize_chat_session()
    return st.session_state.chat_messages

def _format_context_message():
    """
    Format the context message with user data and calculation results
    """
    if not st.session_state.chat_context['calculation_results']:
        return ""
    
    user_data = st.session_state.chat_context['user_data']
    bank_results = st.session_state.chat_context['calculation_results']
    
    # Sort banks by interest rate (highest to lowest)
    sorted_banks = sorted(bank_results, key=lambda x: x['annual_interest'], reverse=True)
    
    context = "Here is the user's financial information and calculation results:\n\n"
    
    # Add user data
    context += f"Savings amount: ${user_data.get('savings_amount', 0):,.2f}\n"
    context += f"Has salary credited: {'Yes' if user_data.get('has_salary', False) else 'No'}\n"
    if user_data.get('has_salary', False):
        context += f"Salary amount: ${user_data.get('salary_amount', 0):,.2f}\n"
    context += f"Card spend: ${user_data.get('spend_amount', 0):,.2f}\n"
    context += f"Bill payments: {user_data.get('giro_count', 0)}\n"
    context += f"Has insurance: {'Yes' if user_data.get('has_insurance', False) else 'No'}\n"
    context += f"Has investments: {'Yes' if user_data.get('has_investments', False) else 'No'}\n\n"
    
    # Add calculation results
    context += "Bank interest calculation results (sorted by highest interest):\n"
    for bank in sorted_banks:
        context += f"- {bank['bank']}: ${bank['annual_interest']:,.2f} per year (${bank['monthly_interest']:,.2f} per month)\n"
    
    return context