import streamlit as st
from script_rapport_sprint import generer_rapport, get_sprint_max
from jira import JIRA
import os


def app():
    #st.set_page_config(page_title="Rapport Sprint JIRA", layout="centered")
    st.title("📋 Générateur de Rapport JIRA")

    email = os.getenv("JIRA_EMAIL")
    api_token = os.getenv("JIRA_API_TOKEN")
    server = "https://charlykaze88.atlassian.net"
    jira = JIRA(server=server, basic_auth=(email, api_token))
    sprint_max = get_sprint_max(jira)

    sprint_input = st.text_input("Numéro du sprint", placeholder="ex: 5")
    if sprint_input and not sprint_input.isdigit():
        st.warning("Veuillez entrer un chiffre uniquement.")

    if st.button("Générer le rapport PDF"):
        if not sprint_input or not sprint_input.isdigit():
            st.error("Le numéro du sprint doit être un entier.")
        else:
            sprint_num = int(sprint_input)
            if sprint_num > sprint_max:
                st.warning("Nous ne sommes pas encore à ce sprint.")
            else:
                filename, error = generer_rapport(sprint_num)
                if error:
                    st.error(error)
                else:
                    st.success("PDF généré avec succès !")
                    with open(filename, "rb") as f:
                        st.download_button("Télécharger le PDF", f, file_name=filename)
