import streamlit as st
import requests
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder

from dotenv import load_dotenv
import os

# Charger le fichier .env
load_dotenv()

# Récupérer la clé API depuis .env
API_KEY = os.getenv("FMP_API_KEY")

COLUMNS_TO_REMOVE = [
    "symbol", "reportedCurrency", "cik", "fillingDate", "acceptedDate", "period"
]

def get_financial_statement(statement_type, ticker):
    """
    Récupère un état financier spécifique depuis Financial Modeling Prep (FMP).
    
    statement_type : "balance-sheet-statement", "income-statement", "cash-flow-statement"
    """
    url = f"https://financialmodelingprep.com/api/v3/{statement_type}/{ticker}?limit=10&apikey={API_KEY}"
    response = requests.get(url)

    try:
        data = response.json()
    except ValueError:
        st.error("⚠️ Erreur lors du parsing JSON de la réponse API FMP.")
        return None

    if not isinstance(data, list) or not data:
        st.error("⚠️ Aucune donnée reçue depuis FMP.")
        return None

    df = pd.DataFrame(data).set_index("date").transpose()
    df = df.drop(index=COLUMNS_TO_REMOVE, errors="ignore")

    # 🔹 **Conversion des chiffres > 1M en milliards**
    def convert_to_billions(value):
        if isinstance(value, (int, float)) and abs(value) > 1_000_000:
            return round(value / 1_000_000_000, 2)  # Conversion en milliards avec 2 décimales
        return value

    df = df.applymap(convert_to_billions)

    # ✅ **Rendre les noms des lignes visibles** (index -> colonne)
    df.insert(0, "Nom du Poste", df.index)  # Déplace l'index en tant que colonne
    df = df.reset_index(drop=True)  # Supprime l'index original

    return df

def display_bilan_page(ticker):
    """
    Affiche la section des bilans comptables avec sélection interactive.
    """
    st.subheader("📑 **État Financier - Standard**")

    selected_statement = st.radio(
        "Sélectionnez un état financier :", 
        ["🏦 Bilan Comptable", "📉 Compte de Résultat", "💸 Flux de Trésorerie"], 
        horizontal=True
    )

    statement_map = {
        "🏦 Bilan Comptable": "balance-sheet-statement",
        "📉 Compte de Résultat": "income-statement",
        "💸 Flux de Trésorerie": "cash-flow-statement",
    }

    statement_data = get_financial_statement(statement_map[selected_statement], ticker)

    if statement_data is not None:
        st.write("### 📊 Données financières (en milliards si > 1M)")

        # 🔹 **Création des options pour AgGrid**
        gb = GridOptionsBuilder.from_dataframe(statement_data)
        gb.configure_default_column(
            resizable=True, 
            cellStyle={"textAlign": "center", "fontWeight": "bold"}  # Centrage + Gras
        )
        gb.configure_grid_options(domLayout='autoHeight', fit_columns_on_grid_load=True)

        # ✅ **Affichage du tableau avec noms des lignes visibles**
        AgGrid(statement_data, gridOptions=gb.build(), height=600, fit_columns_on_grid_load=True)