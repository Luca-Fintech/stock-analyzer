import streamlit as st
from utils.stock_utils import get_stock_info


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

        # Formatage de la market cap en milliards si nécessaire
        market_cap = stock_info["market_cap"]
        if isinstance(market_cap, (int, float)) and market_cap >= 1e9:
            market_cap_str = f"{market_cap / 1e9:.2f} B$"
        elif isinstance(market_cap, (int, float)) and market_cap >= 1e6:
            market_cap_str = f"{market_cap / 1e6:.2f} M$"
        else:
            market_cap_str = "N/A"

        # Affichage principal avec Nom + Ticker
        st.markdown(f"### 🔹 {stock_info['nom']} ({ticker})")

        # Disposition des infos sous forme de colonnes
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.markdown("📂 **Secteur**")
            st.write(f"{stock_info['secteur']}")

        with col2:
            st.markdown("🏭 **Industrie**")
            st.write(f"{stock_info['industrie']}")

        with col3:
            st.markdown("💰 **Cours actuel**")
            st.write(f"{stock_info['cours']} {stock_info['devise']}")

        with col4:
            st.markdown("📉 **Variation journalière**")
            st.write(f"{variation_icon} {variation_str}", unsafe_allow_html=True)

        with col5:
            st.markdown("🏦 **Market Cap**")
            st.write(f"{market_cap_str} ({stock_info['classification']})")

    else:
        st.error("❌ Erreur : Impossible de récupérer les données.")
