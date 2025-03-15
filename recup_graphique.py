import streamlit as st
import plotly.express as px
import pandas as pd
from stock_utils import get_financial_data


def display_financial_graphs(ticker):
    """
    Affiche les graphiques des performances financières avec Plotly.
    """
    data = get_financial_data(ticker)

    if not data:
        st.error("❌ Impossible de récupérer les données financières.")
        return

    years = list(data["years"])

    # 📊 1. Graphique des Marges
    df_marges = pd.DataFrame(
        {
            "Année": years * 3,
            "Marge (%)": list(data["gross_margin"])
            + list(data["operating_margin"])
            + list(data["net_margin"]),
            "Type de Marge": ["Marge Brute"] * len(years)
            + ["Marge Opérationnelle"] * len(years)
            + ["Marge Nette"] * len(years),
        }
    )

    fig_marges = px.bar(
        df_marges,
        x="Année",
        y="Marge (%)",
        color="Type de Marge",
        barmode="group",
        title="📊 Évolution des Marges",
    )
    st.plotly_chart(fig_marges, use_container_width=True)

    # 📈 2. Graphique Revenus & Bénéfice Net
    df_revenue = pd.DataFrame(
        {
            "Année": years * 2,
            "Montant ($)": list(data["total_revenue"]) + list(data["net_income"]),
            "Type": ["Total Revenue"] * len(years) + ["Net Income"] * len(years),
        }
    )

    fig_revenue = px.bar(
        df_revenue,
        x="Année",
        y="Montant ($)",
        color="Type",
        barmode="group",
        title="📈 Total Revenue vs Net Income",
    )
    st.plotly_chart(fig_revenue, use_container_width=True)

    # 📉 3. Graphique Nombre d'Actions en Circulation
    df_shares = pd.DataFrame(
        {"Année": years, "Nombre d'Actions": data["shares_outstanding"]}
    )

    fig_shares = px.line(
        df_shares,
        x="Année",
        y="Nombre d'Actions",
        markers=True,
        title="📉 Nombre d'Actions en Circulation",
    )
    st.plotly_chart(fig_shares, use_container_width=True)

    # 💰 4. Graphique Free Cash Flow vs Net Income
    df_cash = pd.DataFrame(
        {
            "Année": years * 2,
            "Montant ($)": list(data["free_cash_flow"]) + list(data["net_income"]),
            "Type": ["Free Cash Flow"] * len(years) + ["Net Income"] * len(years),
        }
    )

    fig_cash = px.bar(
        df_cash,
        x="Année",
        y="Montant ($)",
        color="Type",
        barmode="group",
        title="💰 Free Cash Flow vs Net Income",
    )
    st.plotly_chart(fig_cash, use_container_width=True)
