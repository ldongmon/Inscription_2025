import streamlit as st
import sqlite3
from datetime import datetime, date
import pandas as pd
from io import BytesIO

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
            acceptation_charte BOOLEAN NOT NULL,
            annee_inscription INTEGER NOT NULL
        )
    """)
    connexion.commit()
    connexion.close()

# Fonction pour enregistrer les données
def enregistrer_donnees(nom, date_naissance, lieu_naissance, telephone, email, consentement_donnees, acceptation_charte, annee_inscription):
    connexion = sqlite3.connect("inscriptions.db")
    curseur = connexion.cursor()
    curseur.execute("""
        INSERT INTO membres (nom, date_naissance, lieu_naissance, telephone, email, consentement_donnees, acceptation_charte, annee_inscription)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (nom, date_naissance, lieu_naissance, telephone, email, consentement_donnees, acceptation_charte, annee_inscription))
    connexion.commit()
    connexion.close()

# Fonction de vérification du mot de passe
def verifier_mot_de_passe(mot_de_passe):
    return mot_de_passe == 'mot_de_passe_admin'

# Fonction pour récupérer toutes les données
def recuperer_donnees():
    connexion = sqlite3.connect("inscriptions.db")
    df = pd.read_sql_query("SELECT * FROM membres", connexion)
    connexion.close()
    return df

# Fonction pour convertir DataFrame en Excel
def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Inscriptions', index=False)
    processed_data = output.getvalue()
    return processed_data

# Initialisation de la base de données
creer_base_de_donnees()

# Interface utilisateur avec Streamlit
st.title("Formulaire d'inscription au 237 KMERCLUB pour l'année 2025")

st.write("Veuillez compléter soigneusement tous les champs du formulaire ci-dessous pour valider votre inscription.")

# Formulaire Streamlit
with st.form("formulaire_inscription"):
    nom = st.text_input("Nom complet*")
    
    # Création du sélecteur de date avec l'année commençant en 1900 et format jour/mois/année
    annee_actuelle = datetime.now().year
    date_naissance = st.date_input(
        "Date de naissance* (JJ/MM/AAAA)",
        min_value=date(1900, 1, 1),
        max_value=date(annee_actuelle, 12, 31),
        value=date(1990, 1, 1),  # Valeur par défaut
        format="DD/MM/YYYY"  # Format jour/mois/année
    )
    
    lieu_naissance = st.text_input("Lieu de naissance*")
    telephone = st.text_input("Téléphone*")
    email = st.text_input("Adresse email*")

    st.write("*Tous les champs sont obligatoires")

    consentement_donnees = st.checkbox("J'accepte la politique de protection des données.*")
    acceptation_charte = st.checkbox("J'accepte les clauses de la charte de l'association.*")

    soumis = st.form_submit_button("Valider mon inscription")

# Traitement des données après soumission
if soumis:
    if not (nom and date_naissance and lieu_naissance and telephone and email):
        st.error("Tous les champs doivent être remplis pour valider votre inscription.")
    elif not (consentement_donnees and acceptation_charte):
        st.error("Vous devez accepter les conditions pour finaliser votre inscription.")
    else:
        try:
            enregistrer_donnees(
                nom,
                date_naissance.strftime("%d/%m/%Y"),  # Format jour/mois/année
                lieu_naissance,
                telephone,
                email,
                consentement_donnees,
                acceptation_charte,
                2025
            )
            st.success("Félicitations ! Votre inscription pour l'année 2025 a été enregistrée avec succès.")
        except Exception as e:
            st.error(f"Une erreur s'est produite lors de l'enregistrement : {str(e)}")

# Section d'authentification pour l'accès administrateur
acces_autorise = False
if st.sidebar.checkbox("Accès administrateur"):
    mot_de_passe = st.sidebar.text_input("Mot de passe", type="password")
    if verifier_mot_de_passe(mot_de_passe):
        st.sidebar.success("Authentification réussie")
        acces_autorise = True
    else:
        st.sidebar.error("Mot de passe incorrect")

# Bouton de téléchargement de la base de données en Excel (accessible uniquement si authentifié)
if acces_autorise:
    if st.button("Télécharger les données en Excel"):
        df = recuperer_donnees()
        excel_file = to_excel(df)
        st.download_button(
            label="Cliquez ici pour télécharger les données en Excel",
            data=excel_file,
            file_name="inscriptions_237_KMERCLUB_2025.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
