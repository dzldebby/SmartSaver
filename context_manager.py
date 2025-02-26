import json
from datetime import datetime

class ChatContextManager:
    """
    Manages the context for AI chat conversations
    """
    def __init__(self, max_history=10):
        self.max_history = max_history
        self.conversation_history = []
        self.user_data = {}
        self.calculation_results = None
        self.last_updated = datetime.now()
    
    def add_message(self, role, content):
        """Add a message to the conversation history"""
        self.conversation_history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        
        # Trim history if it exceeds max length
        if len(self.conversation_history) > self.max_history:
            self.conversation_history = self.conversation_history[-self.max_history:]
        
        self.last_updated = datetime.now()
    
    def update_user_data(self, new_data):
        """Update user data (calculator inputs)"""
        self.user_data.update(new_data)
        self.last_updated = datetime.now()
    
    def update_calculation_results(self, results):
        """Update the calculation results"""
        self.calculation_results = results
        self.last_updated = datetime.now()
    
    def get_formatted_messages(self, system_prompt, include_calculation=True):
        """
        Get formatted messages for the OpenAI API
        """
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add context about user data and calculation results
        context = {
            "user_data": self.user_data
        }
        
        if include_calculation and self.calculation_results:
            context["calculation_results"] = self.calculation_results
        
        # Add context as a system message
        messages.append({
            "role": "system", 
            "content": f"Current user context: {json.dumps(context, default=str)}"
        })
        
        # Add conversation history
        for msg in self.conversation_history:
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        return messages
    
    def clear_history(self):
        """Clear conversation history but keep user data"""
        self.conversation_history = []
        self.last_updated = datetime.now()
    
    def is_context_stale(self, minutes=30):
        """Check if context is stale (hasn't been updated recently)"""
        time_diff = (datetime.now() - self.last_updated).total_seconds() / 60
        return time_diff > minutes