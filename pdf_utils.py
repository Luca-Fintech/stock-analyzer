import fitz  # PyMuPDF
import os


def extract_text_from_pdfs(pdf_files):
    """
    Extrait le texte des fichiers PDF s'ils existent.
    """
    extracted_texts = []

    for pdf in pdf_files:
        try:
            # Vérifier si le fichier est bien chargé
            if pdf is None:
                print(f"⚠️ Fichier PDF non valide : {pdf}")
                continue

            # Ouvrir le fichier PDF
            with fitz.open(stream=pdf.read(), filetype="pdf") as doc:
                text = ""
                for page in doc:
                    text += page.get_text("text") + "\n"
                extracted_texts.append(text)

        except Exception as e:
            print(f"❌ Erreur lors de l'extraction du texte : {e}")

    return extracted_texts
