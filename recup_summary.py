import streamlit as st
from stock_utils import get_stock_summary


def display_stock_summary(ticker):
    """
    Affiche le résumé de l'entreprise après traduction.
    """
    summary = get_stock_summary(ticker)

    st.subheader("📖 **Résumé de l'entreprise**")
    st.write(summary)
