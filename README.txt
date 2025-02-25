# SmartSaver - Bank Interest Rate Optimizer

A sophisticated Python application that helps users optimize their savings by analyzing and recommending the best distribution of funds across different banks based on their tiered interest rates.

## 🌟 Features

- **Interest Rate Optimization**: Automatically calculates the optimal distribution of your savings across multiple banks
- **Multi-Tier Analysis**: Handles complex tiered interest rate structures from different banks
- **Interactive UI**: Built with Streamlit for a user-friendly experience
- **Comparative Analysis**: Shows how the optimized solution compares to equal distribution or single-bank scenarios
- **Detailed Breakdowns**: Provides comprehensive breakdowns of interest calculations and allocations

## 📋 Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/dzldebby/SmartSaver.git
cd SmartSaver
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## 💻 Usage

1. Start the application:
```bash
streamlit run streamlit_app.py
```

2. Enter your total investment amount
3. Click the optimization button to see the recommended distribution
4. Explore detailed breakdowns and comparisons in the interactive UI

## 🏦 Data Format

The application expects bank data in a CSV file (`interest_rates.csv`) with the following structure:

- bank: Bank name
- interest_rate_1: First tier interest rate
- amount_1: First tier maximum amount
- interest_rate_2: Second tier interest rate
- amount_2: Second tier maximum amount
(... and so on for up to 6 tiers)

## 🔧 Technical Architecture

### Interest Rate Processing
- Handles CSV data input
- Processes multi-tier interest rate structures
- Validates and normalizes interest rate data

### Optimization Engine
- Creates and solves linear programming problems
- Implements fallback strategies for edge cases
- Provides detailed allocation breakdowns

### User Interface
- Interactive Streamlit-based interface
- Real-time calculation updates
- Comprehensive result visualization

## 📊 Output Format

The optimizer returns results in the following structure:
```python
{
    'allocations': {
        'BankA': {
            'deposit': float,
            'annual_interest': float,
            'monthly_interest': float,
            'breakdown': [tier_details]
        },
        # ... other banks
    },
    'total_annual_interest': float,
    'total_monthly_interest': float,
    'effective_rate': float
}
```

## 🔍 Error Handling

The application includes comprehensive error handling for:
- CSV loading errors
- Invalid input values
- Calculation errors
- Display errors

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Contact

- Developer: Debby
- GitHub: [@dzldebby](https://github.com/dzldebby)