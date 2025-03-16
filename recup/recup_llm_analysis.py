import ollama
import streamlit as st
import subprocess
from recup.recup_fundamentaux import get_fundamental_ratios
from recup.recup_infos import get_stock_info

def is_ollama_running():
    """
    Vérifie si Ollama tourne déjà en arrière-plan.
    """
    try:
        result = subprocess.run(["pgrep", "-f", "ollama"], stdout=subprocess.PIPE)
        return result.returncode == 0
    except Exception:
        return False

def start_ollama():
    """
    Démarre Ollama uniquement s'il ne tourne pas déjà.
    """
    if not is_ollama_running():
        try:
            subprocess.Popen(["ollama", "serve"])
        except Exception as e:
            st.error(f"❌ Impossible de démarrer Ollama : {e}")

def generate_stock_analysis(ticker):
    """
    Génère une analyse basée sur les critères d'Indépendance AM.
    """
    ratios = get_fundamental_ratios(ticker)
    stock_info = get_stock_info(ticker)

    if not ratios or not stock_info:
        return "❌ Impossible de récupérer les données financières."

    roe = ratios.get("ROE", "N/A")
    per = ratios.get("PER", "N/A")  
    debt_to_equity = ratios.get("Debt-to-Equity", "N/A")
    revenue_growth = ratios.get("Revenue Growth", "N/A")
    market_cap_category = stock_info.get("classification", "N/A")
    net_debt_to_ebitda = ratios.get("NetDebt/EBITDA", "N/A")

    prompt = f"""
    Indépendance AM applique une stratégie 'Quality Value' basée sur :
    - Un ROE élevé (> 12%)
    - Un PER faible (< 12)
    - Une dette maîtrisée (Debt-to-Equity modéré)
    - Une croissance organique positive.
    - Investissement dans les **Small et Mid Caps** uniquement.

    Ratios pour {ticker} :
    - ROE : {roe}%
    - PER : {per}
    - Debt-to-Equity : {debt_to_equity}
    - Net Debt to Ebitda : {net_debt_to_ebitda}
    - Croissance du chiffre d'affaires : {revenue_growth * 100}%
    - Market Cap : {market_cap_category}

    **Question :** L'action {ticker} est-elle un bon candidat pour Indépendance AM ?
    Réponds de façon claire et concise en expliquant si elle respecte leurs critères.
    """

    response = ollama.chat(
        model="gemma3:12b",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.get("message", {}).get("content", "❌ Erreur lors de la génération du rapport.")

def display_stock_analysis(ticker):
    """
    Affiche l’analyse de l’action dans Streamlit.
    """
    st.subheader("📄 **Analyse Indépendance AM**")
    
    with st.spinner("🧠 Analyse en cours..."):
        start_ollama()
        analysis = generate_stock_analysis(ticker)

    st.write(analysis)
