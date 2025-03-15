📊 Stock Analyzer
🚀 Overview
Stock Analyzer is a fundamental analysis tool designed to assess whether a stock meets Independence AM's investment criteria.
It uses Financial Modeling Prep (FMP) to fetch financial statements and calculate key financial ratios for stock evaluation.
----------------------------------------------------------------------------------------------------------------------------
The interface is built with Streamlit, and Poetry is used for dependency management, making installation and deployment easy.

📌 Installation & Setup
1️⃣ Clone the repository

git clone https://github.com/Luca-Fintech/stock-analyzer.git
cd stock-analyzer
2️⃣ Install Poetry (if not already installed)
If Poetry is not installed on your system, run:

curl -sSL https://install.python-poetry.org | python3 -
Then verify the installation:

poetry --version
3️⃣ Install dependencies
Inside the project folder, run:

poetry install
This will install all required dependencies in an isolated environment.

4️⃣ Set up Financial Modeling Prep API key
The project uses Financial Modeling Prep (FMP) to fetch financial data.
You need to add your API key in an .env file:

Create an .env file in the project folder:

touch .env
Add your API key inside:

API_KEY=your_fmp_api_key
Make sure .env is added to .gitignore to prevent accidentally pushing your API key to GitHub.

🎯 Usage
1️⃣ Run the application
Inside the project folder, run:

poetry run streamlit run app.py
This will launch the user interface in your web browser.

2️⃣ Select a stock
Enter the ticker of the stock you want to analyze (e.g., AAPL, MSFT, TSLA).
The application will display:
📊 Fundamental ratios (ROE, ROIC, PER, EV/EBITDA, etc.)
📑 Financial statements (Balance Sheet, Income Statement, Cash Flow Statement)
🤖 LLM Analysis for processing financial reports using AI.
3️⃣ Evaluate if the stock meets Independence AM’s criteria
Analyze the calculated ratios.
Compare them to Independence AM’s investment criteria to determine if the stock qualifies for purchase.
🛠 Features
✅ Fetch fundamental financial data via Financial Modeling Prep (FMP)
✅ Clear and interactive interface with Streamlit
✅ Organized into three categories:

Fundamental Info 📊
Financial Statements 📑
LLM Analysis 🤖
✅ View 5 years of financial statements
✅ Interactive data tables
