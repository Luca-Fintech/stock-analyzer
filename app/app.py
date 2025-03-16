import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st

st.set_page_config(page_title="📊 Stock Analyzer", layout="wide")

from recup.recup_ticker import get_ticker
from recup.recup_infos import display_stock_info
from recup.recup_summary import display_stock_summary
from recup.recup_fundamentaux import display_fundamental_ratios
from recup.recup_graphique import display_financial_graphs
from recup.recup_llm import process_pdfs_with_llm
from recup.bilan_page import display_bilan_page  
from recup.recup_llm_analysis import display_stock_analysis

st.title("📊 Independance AM - Stock analyzer")

ticker = get_ticker()

if ticker:
    display_stock_info(ticker)

    st.markdown("---")

    selected_section = st.radio(
        "Sélectionnez une section :",
        ["📊 Info Fondamentale", "📑 Bilan", "🧠 LLM"],
        horizontal=True,
    )

    st.markdown("---")

    if selected_section == "📊 Info Fondamentale":
        display_stock_summary(ticker)
        st.markdown("---")
        display_fundamental_ratios(ticker)
        st.markdown("---")
        display_financial_graphs(ticker)
        st.markdown("---")
        display_stock_analysis(ticker)

    elif selected_section == "📑 Bilan":
        display_bilan_page(ticker)

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
