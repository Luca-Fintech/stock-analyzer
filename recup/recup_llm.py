import ollama
import streamlit as st
import subprocess
from utils.pdf_utils import extract_text_from_pdfs
from utils.stock_utils import get_stock_summary


def is_ollama_running():
    """
    Vérifie si Ollama tourne déjà en arrière-plan.
    """
    try:
        result = subprocess.run(["pgrep", "-f", "ollama"], stdout=subprocess.PIPE)
        return result.returncode == 0  # Si 0, Ollama est en cours d'exécution
    except Exception:
        return False  # En cas d'erreur, on considère que Ollama ne tourne pas


def start_ollama():
    """
    Démarre Ollama uniquement s'il ne tourne pas déjà.
    """
    if not is_ollama_running():
        try:
            subprocess.Popen(["ollama", "serve"])
        except Exception as e:
            st.error(f"❌ Impossible de démarrer Ollama : {e}")

def process_pdfs_with_llm(pdf_files, ticker):
    """
    Génère un compte-rendu ultra détaillé et structuré avec une analyse sectorielle et des perspectives futures.
    """
    st.subheader("🧠 Analyse de l'Historique avec l'IA")
    with st.spinner("L'IA analyse l'entreprise en profondeur... ⏳"):
        try:
            # 🔍 Extraction des textes des PDF
            pdf_texts = extract_text_from_pdfs(pdf_files)

            # 📊 Récupération du résumé de l'entreprise
            company_summary = get_stock_summary(ticker)

            # 🏢 Contexte du Secteur
            sector_context = f"L'entreprise est dans le secteur suivant : {ticker}. Voici son résumé : {company_summary}."

            # 🧠 🔥 Nouveau Prompt Ultra Structuré 🔥
            prompt = f"""
            🎯 **Objectif** : Faire un **compte-rendu détaillé et structuré** des **dernières années**, basé sur les données des **rapports financiers et earnings calls** fournis.

            🔹 **Contexte** : L’IA a accès aux **rapports financiers** et **earnings calls** suivants :
            {''.join(pdf_texts)}

            🔹 **Mission** : Écrire un **compte-rendu ultra précis** qui suit **un fil conducteur logique**, 
            en expliquant **année par année** :
            - 🏭 **Contexte sectoriel** : Quels étaient les défis/opportunités du secteur cette année-là ?
            - 📊 **Performances financières** : Résultats, croissance, marges, tendances clés ?
            - 📢 **Événements marquants** : Fusions, acquisitions, nouveaux produits, décisions stratégiques ?
            - 🔄 **Lien avec les années précédentes** : Évolution des stratégies et impact sur les années suivantes ?

            🔹 **Informations à extraire** :
            - 📅 **Identifier automatiquement les années concernées** en fonction des données trouvées.
            - 📊 **Analyser les tendances et les performances financières** en reliant les événements marquants.
            - 🚀 **Fournir des perspectives à date** : Quelle est la stratégie actuelle ? Quels sont les défis/opportunités à venir ?

            🔹 **Format attendu** :
            ---
            🏆 **Année détectée : XXXX** (la plus récente)
            - 📊 **Performance financière** : [Chiffres clés]
            - 🏭 **Contexte sectoriel** : [Tendances et dynamique du marché]
            - 📢 **Événements majeurs** : [Décisions stratégiques, lancements, acquisitions]
            - 🔄 **Impact futur** : [Influence sur les années suivantes]

            🏆 **Année détectée : XXXX** (année précédente)
            - [Mêmes éléments]

            🏆 **Années précédentes** (jusqu'à 4 ans en arrière)
            - [Mêmes éléments]

            🚀 **Perspectives actuelles et tendances à venir**
            - 🔮 **Vision du management** : [Plans stratégiques]
            - 📊 **Enjeux sectoriels** : [Opportunités et menaces]
            - 🔄 **Impact sur les résultats futurs** : [Prévisions et incertitudes]

            🔥 **Ta mission** : Génère un **compte-rendu ultra détaillé** avec cette structure. 
            - **Analyse chaque année sans que je te les donne explicitement.**
            - **Construis un fil rouge logique pour montrer l'évolution.**
            - **Ajoute une section de perspectives pour anticiper le futur.**
            """

            # 🔥 Envoi à Ollama avec `gemma3:12b`
            response = ollama.chat(
                model="gemma3:12b", messages=[{"role": "user", "content": prompt}]
            )

            # 📢 Affichage du Résumé
            st.markdown("### 📜 Compte-Rendu Historique et Perspectives")
            st.write(response["message"]["content"])

        except Exception as e:
            st.error(f"❌ Erreur lors du traitement des PDFs avec l'IA : {e}")
