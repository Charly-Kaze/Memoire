import streamlit as st
from script_rapport_sprint import generer_rapport  # on appelle la fonction directement
import os

def app():
    #st.set_page_config(page_title="Rapport Sprint JIRA", layout="centered")
    st.title("Générateur de Rapport JIRA")
    
    st.markdown("Clique sur le bouton ci-dessous pour générer le rapport PDF du sprint.")
    
    if st.button("Générer le rapport PDF"):
        try:
            generer_rapport()  # appel direct de ta logique
            st.success("PDF généré avec succès !")
    
            if os.path.exists("rapport_sprint.pdf"):
                with open("rapport_sprint.pdf", "rb") as f:
                    st.download_button("Télécharger le PDF", f, file_name="rapport_sprint.pdf")
            else:
                st.warning("Le fichier PDF n'a pas été trouvé.")
        except Exception as e:
            st.error(f"Erreur lors de la génération : {e}")
