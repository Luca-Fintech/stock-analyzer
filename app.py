import streamlit as st

# 📌 `st.set_page_config()` DOIT être appelé en premier
st.set_page_config(page_title="📊 Stock Analyzer", layout="centered")

from recup_ticker import get_ticker
from recup_infos import display_stock_info
from recup_summary import display_stock_summary
from recup_fundamentaux import display_fundamental_ratios
from recup_graphique import display_financial_graphs
from recup_llm import process_pdfs_with_llm
from bilan_page import display_bilan_page  # 🔥 Importation de la gestion des bilans

# 📌 Titre de l'application
st.title("📊 Stock Analyzer")

ticker = get_ticker()

if ticker:
    # 📄 Affichage des informations générales
    display_stock_info(ticker)

    # 📌 Séparation visuelle
    st.markdown("---")

    # 🚀 Boutons de navigation
    selected_section = st.radio(
        "Sélectionnez une section :", 
        ["📊 Info Fondamentale", "📑 Bilan", "🧠 LLM"], 
        horizontal=True
    )

    st.markdown("---")

    # 📊 Info Fondamentale
    if selected_section == "📊 Info Fondamentale":
        display_stock_summary(ticker)
        st.markdown("---")
        display_fundamental_ratios(ticker)
        st.markdown("---")
        display_financial_graphs(ticker)

    # 📑 Bilan Comptable (appel à `bilan_page.py`)
    elif selected_section == "📑 Bilan":
        display_bilan_page(ticker)

    # 🧠 Analyse LLM
    elif selected_section == "🧠 LLM":
        st.subheader("📂 Ajoutez des rapports financiers et earnings calls")
        uploaded_files = st.file_uploader(
            "Téléchargez jusqu'à 8 fichiers PDF", type="pdf", accept_multiple_files=True
        )

        if uploaded_files:
            if len(uploaded_files) > 8:
                st.warning("⚠️ Vous ne pouvez ajouter que 8 fichiers maximum.")
            else:
                process_pdfs_with_llm(uploaded_files, ticker)