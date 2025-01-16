import streamlit as st
import sqlite3

# Configuration de la base de données
def creer_base_de_donnees():
    connexion = sqlite3.connect("inscriptions.db")
    curseur = connexion.cursor()
    curseur.execute("""
        CREATE TABLE IF NOT EXISTS membres (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            date_naissance TEXT NOT NULL,
            lieu_naissance TEXT NOT NULL,
            telephone TEXT NOT NULL,
            email TEXT NOT NULL,
            consentement_donnees BOOLEAN NOT NULL,
            acceptation_charte BOOLEAN NOT NULL
        )
    """)
    connexion.commit()
    connexion.close()

# Fonction pour enregistrer les données
def enregistrer_donnees(nom, date_naissance, lieu_naissance, telephone, email, consentement_donnees, acceptation_charte):
    connexion = sqlite3.connect("inscriptions.db")
    curseur = connexion.cursor()
    curseur.execute("""
        INSERT INTO membres (nom, date_naissance, lieu_naissance, telephone, email, consentement_donnees, acceptation_charte)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (nom, date_naissance, lieu_naissance, telephone, email, consentement_donnees, acceptation_charte))
    connexion.commit()
    connexion.close()

# Interface utilisateur avec Streamlit
st.title("Formulaire d'inscription")

# Formulaire Streamlit
with st.form("formulaire_inscription"):
    nom = st.text_input("Nom complet")
    date_naissance = st.date_input("Date de naissance")
    lieu_naissance = st.text_input("Lieu de naissance")
    telephone = st.text_input("Téléphone")
    email = st.text_input("Adresse email")

    # Cases à cocher pour le consentement
    consentement_donnees = st.checkbox("J'accepte la politique de protection des données.")
    acceptation_charte = st.checkbox("J'accepte les clauses de la charte de l'association.")

    # Bouton de soumission
    soumis = st.form_submit_button("S'inscrire")

# Traitement des données après soumission
if soumis:
    if not (nom and date_naissance and lieu_naissance and telephone and email):
        st.error("Tous les champs doivent être remplis.")
    elif not (consentement_donnees and acceptation_charte):
        st.error("Vous devez accepter les conditions.")
    else:
        enregistrer_donnees(
            nom,
            date_naissance.strftime("%Y-%m-%d"),
            lieu_naissance,
            telephone,
            email,
            consentement_donnees,
            acceptation_charte
        )
        st.success("Inscription enregistrée avec succès!")

# Initialisation de la base de données
creer_base_de_donnees()