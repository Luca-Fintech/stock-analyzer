import streamlit as st


def get_ticker():
    """
    Demande à l'utilisateur de saisir un ticker et le retourne.
    """
    return st.text_input("🔍 Entrez le ticker de l'action :")
