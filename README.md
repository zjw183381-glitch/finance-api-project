# Finance API Environment Project

## Project Objective

This project initializes an isolated Python development environment for accessing financial and economic data.

The project connects to:

- Federal Reserve Economic Data (FRED)
- Yahoo Finance
- Alpha Vantage

## Technology Stack

- Python
- Git
- GitHub
- Python Virtual Environment (venv)
- Terminal CLI

## Project Files

- main.py - Tests API connectivity and prints results in JSON format.
- requirements.txt - Contains the required Python packages.
- .gitignore - Prevents API keys and virtual environment files from being uploaded.

## Setup Instructions

1. Create a virtual environment:

python -m venv venv

2. Activate the virtual environment on Windows:

venv\Scripts\activate

3. Install dependencies:

pip install -r requirements.txt

4. Create a .env file and add:

FRED_API_KEY=your_fred_api_key

ALPHA_VANTAGE_API_KEY=your_alpha_vantage_api_key

5. Run the connectivity test:

python main.py

## Security

API keys are stored locally in the .env file. The .env file is excluded from Git tracking through .gitignore.
