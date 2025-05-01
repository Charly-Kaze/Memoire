import streamlit as st
import psycopg2
from streamlit_extras.switch_page_button import switch_page

# Connexion PostgreSQL
def connect_db():
    return psycopg2.connect(
        host="DB_HOST",
        database="DB_NAME",
        user="DB_USER",
        port="DB_PORT",
        password="DB_PASSWORD"
    )

# Configuration page
st.set_page_config(page_title="Connexion", layout="centered")
st.title("🔐 Connexion à l'application")

if "reset_mode" not in st.session_state:
    st.session_state.reset_mode = False

# Connexion standard
if not st.session_state.reset_mode:
    with st.form("login_form"):
        nom = st.text_input("Nom")
        email = st.text_input("Email")
        mdp = st.text_input("Mot de passe", type="password")

        col1, col2 = st.columns(2)
        with col1:
            submit = st.form_submit_button("Se connecter")
        with col2:
            reset = st.form_submit_button("Réinitialiser")

    if submit:
        if nom and email and mdp:
            conn = connect_db()
            cur = conn.cursor()
            cur.execute("SELECT Nom, MDP FROM Users WHERE email = %s", (email,))
            row = cur.fetchone()
            if row and row[0] == nom and row[1] == mdp:
                st.success(f"Bienvenue, {Nom} !")
                # Authentifié avec succès
                st.success("Connexion réussie ! Redirection...")
                st.session_state["auth"] = True
                st.switch_page("UI") 
            else:
                st.error("Identifiants invalides.")
            cur.close()
            conn.close()
        else:
            st.error("Tous les champs sont requis.")

    if reset:
        st.session_state.reset_mode = True
        st.experimental_rerun()

# Réinitialisation
else:
    st.subheader("🔁 Réinitialisation du mot de passe")
    email = st.text_input("Email")
    new_mdp = st.text_input("Nouveau mot de passe", type="password")
    confirm_mdp = st.text_input("Confirmer le mot de passe", type="password")

    col1, col2 = st.columns(2)
    if col1.button("Valider"):
        if new_mdp == confirm_mdp and new_mdp:
            conn = connect_db()
            cur = conn.cursor()
            cur.execute("SELECT * FROM Users WHERE email = %s", (email,))
            if cur.fetchone():
                cur.execute("UPDATE Users SET MDP = %s WHERE email = %s", (new_mdp, email))
                conn.commit()
                st.success("Mot de passe mis à jour avec succès.")
                cur.close()
                conn.close()
                st.session_state.reset_mode = False
                st.experimental_rerun()
            else:
                st.error("Email non trouvé.")
                cur.close()
                conn.close()
        else:
            st.error("Les mots de passe ne correspondent pas ou sont vides.")

    if col2.button("Annuler"):
        st.session_state.reset_mode = False
        st.experimental_rerun()
