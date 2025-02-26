# test_context_manager.py
from context_manager import ChatContextManager
import json

# Create a context manager
context = ChatContextManager()

# Add user data
context.update_user_data({
    "savings_amount": 50000,
    "has_salary": True,
    "spend_amount": 500,
    "giro_count": 3
})

# Add calculation results
context.update_calculation_results([
    {
        "bank": "UOB One",
        "annual_interest": 1800.00,
        "monthly_interest": 150.00
    },
    {
        "bank": "OCBC 360",
        "annual_interest": 1650.00,
        "monthly_interest": 137.50
    }
])

# Add some messages
context.add_message("user", "Which bank gives me the best interest rate?")
context.add_message("assistant", "Based on your profile, UOB One offers the highest interest rate at $1,800 annually.")
context.add_message("user", "Why is that?")

# Get formatted messages
system_prompt = "You are a helpful financial assistant for SmartSaverSG."
messages = context.get_formatted_messages(system_prompt)

# Print the formatted messages
print("Formatted Messages for OpenAI API:")
print(json.dumps(messages, indent=2))

# Test context staleness
print("\nIs context stale?", context.is_context_stale(minutes=5))