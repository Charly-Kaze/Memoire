import streamlit as st
import subprocess
import os

st.set_page_config(page_title="Rapport Sprint JIRA", layout="centered")
st.title("Générateur de Rapport JIRA")

# Message d'instruction
st.markdown("Clique sur le bouton ci-dessous pour générer le rapport PDF du sprint.")

if st.button("Générer le rapport PDF"):
    try:
        result = subprocess.run(["python", "script_rapport_sprint.py"], check=True)
        st.success("PDF généré avec succès !")

        # Lien de téléchargement si fichier présent
        if os.path.exists("rapport_sprint.pdf"):
            with open("rapport_sprint.pdf", "rb") as f:
                st.download_button("Télécharger le PDF", f, file_name="rapport_sprint.pdf")
        else:
            st.warning("Le fichier PDF n'a pas été trouvé.")
    except subprocess.CalledProcessError:
        st.error("Erreur lors de l'exécution du script.")
