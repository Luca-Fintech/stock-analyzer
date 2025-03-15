import streamlit as st
from stock_utils import get_stock_info


def display_stock_info(ticker):
    """
    Récupère et affiche les informations de base d'un stock avec un affichage amélioré.
    """
    stock_info = get_stock_info(ticker)

    if stock_info:
        # Définition de l'icône de variation 📉📈
        variation = stock_info["variation"]
        variation_str = f"{variation:.2f}%"
        variation_icon = "🔺" if variation > 0 else "🔻"

        # Affichage principal avec Nom + Ticker
        st.markdown(f"### 🔹 {stock_info['nom']} ({ticker})")

        # Disposition des infos sous forme de colonnes
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown("📂 **Secteur**")
            st.write(f"{stock_info['secteur']}")

        with col2:
            st.markdown("🏭 **Industrie**")
            st.write(f"{stock_info['industrie']}")

        with col3:
            st.markdown("💰 **Cours actuel**")
            st.write(
                f"{stock_info['cours']} {stock_info['devise']}"
            )  # Ajout de la devise

        with col4:
            st.markdown("📉 **Variation journalière**")
            st.write(f"{variation_icon} {variation_str}", unsafe_allow_html=True)
    else:
        st.error("❌ Erreur : Impossible de récupérer les données.")
