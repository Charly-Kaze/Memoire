import streamlit as st
import psycopg2
from multiapp import MultiApp
import UI

def connect_db():
    return psycopg2.connect(
        host="aws-0-eu-west-3.pooler.supabase.com",
        database="postgres",
        user="postgres.pcgddrgfhlkaltzipyah",
        port=6543,
        password="jeAYs249tiN)G2S"
    )

st.title("🔐 Connexion à l'application")


st.set_page_config(page_title="Connexion", layout="centered")

if "auth" not in st.session_state:
    st.session_state.auth = False
if "reset_mode" not in st.session_state:
    st.session_state.reset_mode = False

# Authentifié : accès à l'app
if st.session_state.auth:
    app = MultiApp()
    app.add_app("UI", UI.app)
    app.run()

# Connexion
elif not st.session_state.reset_mode:
    with st.form("login_form"):
        nom = st.text_input("Nom")
        email = st.text_input("Email")
        mdp = st.text_input("Mot de passe", type="password")

        col1, col2 = st.columns(2)
        submit = col1.form_submit_button("Se connecter")
        reset = col2.form_submit_button("Réinitialiser")

    if submit:
        if nom and email and mdp:
            try:
                conn = connect_db()
                cur = conn.cursor()
                cur.execute('SELECT "Nom", "MDP" FROM "Users" WHERE email = %s', (email,))
                row = cur.fetchone()
                if row and row[0] == nom and row[1] == mdp:
                    st.session_state.auth = True
                    st.rerun()
                else:
                    st.error("Identifiants invalides.")
            except Exception as e:
                st.error("Erreur de connexion.")
                st.exception(e)
            finally:
                if 'cur' in locals(): cur.close()
                if 'conn' in locals(): conn.close()
        else:
            st.error("Tous les champs sont requis.")

    if reset:
        st.session_state.reset_mode = True
        st.rerun()

# Réinitialisation du mot de passe
else:
    st.subheader("🔁 Réinitialisation du mot de passe")
    with st.form("reset_form"):
        email = st.text_input("Email")
        new_mdp = st.text_input("Nouveau mot de passe", type="password")
        confirm_mdp = st.text_input("Confirmer le mot de passe", type="password")

        valider = st.form_submit_button("Valider")
        annuler = st.form_submit_button("Annuler")

    if valider:
        if new_mdp == confirm_mdp and new_mdp:
            try:
                conn = connect_db()
                cur = conn.cursor()
                cur.execute('SELECT * FROM "Users" WHERE email = %s', (email,))
                if cur.fetchone():
                    cur.execute('UPDATE "Users" SET "MDP" = %s WHERE email = %s', (new_mdp, email))
                    conn.commit()
                    st.success("Mot de passe mis à jour.")
                    st.session_state.reset_mode = False
                    st.rerun()
                else:
                    st.error("Email non trouvé.")
            except Exception as e:
                st.error("Erreur lors de la mise à jour.")
                st.exception(e)
            finally:
                if 'cur' in locals(): cur.close()
                if 'conn' in locals(): conn.close()
        else:
            st.error("Les mots de passe ne correspondent pas ou sont vides.")

    if annuler:
        st.session_state.reset_mode = False
        st.rerun()
