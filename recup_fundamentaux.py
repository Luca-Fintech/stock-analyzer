import streamlit as st
from stock_utils import get_fundamental_ratios


def display_fundamental_ratios(ticker):
    """
    Affiche les ratios financiers clés d'une entreprise.
    """
    ratios = get_fundamental_ratios(ticker)

    if ratios:
        st.markdown(f"## 📊 Analyse Fondamentale - {ticker}")
        
        st.subheader("💰 **Valorisation**")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                "PER",
                f"{ratios['PER']:.2f}" if isinstance(ratios["PER"], (int, float)) else "N/A",
            )
        with col2:
            st.metric(
                "EV/EBITDA",
                f"{ratios['EV/EBITDA']:.2f}" if isinstance(ratios["EV/EBITDA"], (int, float)) else "N/A",
            )
        with col3:
            st.metric(
                "Earnings Yield",
                f"{ratios['Earnings Yield']:.2%}" if isinstance(ratios["Earnings Yield"], (int, float)) else "N/A",
            )

        st.subheader("💸 **Free Cash Flow & BFR**")
        col4, col5, col6 = st.columns(3)
        with col4:
            st.metric(
                "FCF Yield",
                f"{ratios['Free Cash Flow Yield']:.2%}" if isinstance(ratios["Free Cash Flow Yield"], (int, float)) else "N/A",
            )
        with col5:
            st.metric(
                "Capex/Revenue",
                f"{ratios['Capex/Revenue']:.2%}" if isinstance(ratios["Capex/Revenue"], (int, float)) else "N/A",
            )
        with col6:
            st.metric(
                "Working Capital Ratio",
                f"{ratios['Working Capital Ratio']:.2%}" if isinstance(ratios["Working Capital Ratio"], (int, float)) else "N/A",
            )

        # 🏦 **Profitabilité**
        st.subheader("🏦 **Profitabilité**")
        col7, col_mid_1, col8 = st.columns([1, 1, 1])  # Alignement avec la colonne centrale des sections à 3 colonnes
        with col7:
            st.metric(
                "ROE",
                f"{ratios['ROE']:.2%}" if isinstance(ratios["ROE"], (int, float)) else "N/A",
            )
        with col_mid_1:
            st.metric(
                "ROIC",
                f"{ratios['ROIC']:.2%}" if isinstance(ratios["ROIC"], (int, float)) else "N/A",
            )

        # 📈 **Croissance**
        st.subheader("📈 **Croissance**")
        col9, col_mid_2, col10 = st.columns([1, 1, 1])  # Alignement avec la colonne du milieu des sections à 3 colonnes
        with col9:
            st.metric(
                "EPS Growth",
                f"{ratios['EPS Growth']:.2%}" if isinstance(ratios["EPS Growth"], (int, float)) else "N/A",
            )
        with col_mid_2:
            st.metric(
                "Revenue Growth",
                f"{ratios['Revenue Growth']:.2%}" if isinstance(ratios["Revenue Growth"], (int, float)) else "N/A",
            )
    else:
        st.error("❌ Erreur : Impossible de récupérer les données fondamentales.")

