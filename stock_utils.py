import yfinance as yf
from deep_translator import GoogleTranslator
import requests

from dotenv import load_dotenv
import os

# Charger le fichier .env
load_dotenv()

# Récupérer la clé API depuis .env
API_KEY = os.getenv("FMP_API_KEY")

if not API_KEY:
    raise ValueError("❌ Clé API FMP manquante ! Vérifie ton fichier .env.")
else:
    print("Clé récupéré avec succès")


def get_stock_info(ticker):
    """
    Récupère les informations clés d'une action via yfinance.
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        return {
            "nom": info.get("longName", "N/A"),
            "secteur": info.get("sector", "N/A"),
            "industrie": info.get("industry", "N/A"),  # Ajout de l'industrie
            "cours": info.get("regularMarketPrice", "N/A"),
            "variation": info.get("regularMarketChangePercent", 0.0),
            "devise": info.get("currency", "N/A"),  # Ajout de la devise
        }
    except Exception as e:
        print(f"Erreur lors de la récupération des données : {e}")
        return None


import requests
import yfinance as yf
from dotenv import load_dotenv
import os

# Charger la clé API depuis .env
load_dotenv()
API_KEY = os.getenv("FMP_API_KEY")

if not API_KEY:
    raise ValueError("❌ Clé API FMP manquante ! Vérifie ton fichier .env.")


def get_fundamental_ratios(ticker):
    """
    Récupère les ratios financiers clés pour une analyse fondamentale,
    combinant Financial Modeling Prep (FMP) et Yahoo Finance.
    """
    try:
        print(f"🔍 Récupération des données pour {ticker}")

        # 📡 1. Requête unique à Financial Modeling Prep (FMP)
        url = f"https://financialmodelingprep.com/api/v3/key-metrics/{ticker}?apikey={API_KEY}"
        print(f"📡 Envoi de la requête API FMP : {url}")  # Debug

        try:
            response = requests.get(url)
            fmp_data = response.json()

            if not fmp_data or "error" in fmp_data:
                print(
                    f"⚠️ Erreur avec l'API FMP : {fmp_data.get('error', 'Données non disponibles')}"
                )
                fmp_data = [{}]  # Valeurs par défaut si l'API ne fonctionne pas

            # On prend les données de la dernière année disponible
            latest_metrics = (
                fmp_data[0] if isinstance(fmp_data, list) and fmp_data else {}
            )

            # 🔹 Récupération des valeurs depuis FMP
            roic = latest_metrics.get("roic", "N/A")
            net_debt_to_ebitda = latest_metrics.get("netDebtToEBITDA", "N/A")
            roe = latest_metrics.get("roe", "N/A")
            per = latest_metrics.get("peRatio", "N/A")
            ev_ebitda = latest_metrics.get("enterpriseValueOverEBITDA", "N/A")
            debt_to_equity = latest_metrics.get("debtToEquity", "N/A")
            dividend_yield = latest_metrics.get("dividendYield", "N/A")
            payout_ratio = latest_metrics.get("payoutRatio", "N/A")

            # 🔹 Nouveaux ratios
            working_capital = latest_metrics.get("workingCapital", "N/A")
            free_cash_flow_yield = latest_metrics.get("freeCashFlowYield", "N/A")
            capex_to_revenue = latest_metrics.get("capexToRevenue", "N/A")
            cash_conversion_cycle = latest_metrics.get("cashConversionCycle", "N/A")
            earnings_yield = latest_metrics.get("earningsYield", "N/A")
            roce = latest_metrics.get("returnOnCapitalEmployed", "N/A")  # 🆕 Ajouté

        except Exception as e:
            print(f"❌ Erreur lors de la récupération des données FMP : {e}")
            roic = net_debt_to_ebitda = roe = per = ev_ebitda = debt_to_equity = "N/A"
            dividend_yield = payout_ratio = working_capital = free_cash_flow_yield = (
                capex_to_revenue
            ) = "N/A"
            cash_conversion_cycle = earnings_yield = roce = "N/A"

        # 🔍 2. Récupération des données Yahoo Finance pour MarketCap/Revenue et Croissance
        stock = yf.Ticker(ticker)
        info = stock.info

        # 📌 MarketCap/Total Revenue uniquement avec Yahoo Finance
        market_cap_to_revenue = (
            info.get("marketCap", "N/A") / info.get("totalRevenue", 1)
            if info.get("totalRevenue")
            else "N/A"
        )

        # 📌 EPS Growth et Revenue Growth uniquement avec Yahoo Finance
        eps_growth = info.get("earningsQuarterlyGrowth", "N/A")
        revenue_growth = info.get("revenueGrowth", "N/A")

        # 📌 Working Capital Ratio (BFR / Revenue)
        if working_capital != "N/A" and isinstance(market_cap_to_revenue, (int, float)):
            working_capital_ratio = working_capital / info.get("totalRevenue")
        else:
            working_capital_ratio = "N/A"

        # Retour des ratios fondamentaux
        return {
            "ROE": roe,
            "ROIC": roic,
            "PER": per,
            "MarketCap/Total Revenue": market_cap_to_revenue,
            "EV/EBITDA": ev_ebitda,
            "Debt-to-Equity": debt_to_equity,
            "NetDebt/EBITDA": net_debt_to_ebitda,
            "EPS Growth": eps_growth,
            "Revenue Growth": revenue_growth,
            "Dividend Yield": dividend_yield,
            "Payout Ratio": payout_ratio,
            "Working Capital Ratio": working_capital_ratio,
            "Free Cash Flow Yield": free_cash_flow_yield,
            "Capex/Revenue": capex_to_revenue,
            "Cash Conversion Cycle": cash_conversion_cycle,
            "Earnings Yield": earnings_yield,
            "Return on Capital Employed (ROCE)": roce,
        }

    except Exception as e:
        print(f"❌ Erreur lors de la récupération des ratios fondamentaux : {e}")
        return None


def get_stock_summary(ticker):
    """
    Récupère le résumé de l'entreprise en anglais et le traduit en français.
    """
    try:
        stock = yf.Ticker(ticker)
        summary = stock.info.get("longBusinessSummary", "Résumé non disponible.")
        # Traduction en français
        translated_summary = GoogleTranslator(source="en", target="fr").translate(
            summary
        )

        return translated_summary
    except Exception as e:
        print(f"Erreur lors de la récupération du résumé : {e}")
        return "Résumé non disponible."


def get_financial_data(ticker):
    """
    Récupère les données financières pour afficher les graphiques.
    """
    try:
        stock = yf.Ticker(ticker)

        # Récupération des états financiers
        income_stmt = stock.financials
        balance_sheet = stock.balance_sheet
        cash_flow = stock.cashflow

        # Extraction des dernières années disponibles
        years = income_stmt.columns[:4]  # On prend les 4 dernières années

        data = {
            "years": years[
                ::-1
            ],  # On inverse pour avoir les années dans l'ordre croissant
            "gross_margin": (
                income_stmt.loc["Gross Profit"] / income_stmt.loc["Total Revenue"]
            ).iloc[:4][::-1],
            "operating_margin": (
                income_stmt.loc["Operating Income"] / income_stmt.loc["Total Revenue"]
            ).iloc[:4][::-1],
            "net_margin": (
                income_stmt.loc["Net Income"] / income_stmt.loc["Total Revenue"]
            ).iloc[:4][::-1],
            "total_revenue": income_stmt.loc["Total Revenue"].iloc[:4][::-1],
            "net_income": income_stmt.loc["Net Income"].iloc[:4][::-1],
            "shares_outstanding": balance_sheet.loc["Ordinary Shares Number"].iloc[:4][
                ::-1
            ],
            "free_cash_flow": cash_flow.loc["Free Cash Flow"].iloc[:4][::-1],
        }

        return data

    except Exception as e:
        print(f"Erreur lors de la récupération des données financières : {e}")
        return None
