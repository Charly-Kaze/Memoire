import streamlit as st

# Configuration de la page
st.set_page_config(page_title="Connexion", layout="centered")

# Titre
st.title("🔐 Connexion à l'application")

# Formulaire de connexion
with st.form("login_form"):
    nom = st.text_input("Nom")
    email = st.text_input("Email")
    mdp = st.text_input("Mot de passe", type="password")

    # Deux boutons
    bouton_connexion, bouton_reset = st.columns(2)
    with bouton_connexion:
        submit = st.form_submit_button("Se connecter")

    with bouton_reset:
        reset = st.form_submit_button("Réinitialiser")

# Actions
if submit:
    if nom and email and mdp:
        st.success(f"Bienvenue, {nom} !")
        # Tu peux ici ajouter une vérification avec une base de données
    else:
        st.error("Tous les champs sont requis.")

if reset:
    st.experimental_rerun()
