import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Test Pressostats", layout="centered")
st.title("Formulaire de Test - Pressostats à Membrane")

csv_file = "tests_pressostats.csv"

# Chargement sécurisé des données
if "data" not in st.session_state:
    if os.path.exists(csv_file) and os.path.getsize(csv_file) > 0:
        try:
            df_loaded = pd.read_csv(csv_file, sep=';', encoding='utf-8-sig')
            st.session_state.data = df_loaded.to_dict(orient="records")
        except pd.errors.EmptyDataError:
            st.warning("Le fichier CSV est vide ou corrompu. Il sera réinitialisé.")
            st.session_state.data = []
    else:
        st.session_state.data = []

# Formulaire d’entrée
with st.form("formulaire_test"):
    col1, col2 = st.columns(2)
    with col1:
        id = st.text_input("Numéro Pressostat")
        date = st.date_input("Date de test")
        testeur = st.text_input("Testé par")
        declenchement = st.number_input("Pression en montée (bar)", step=0.01)
        retour = st.number_input("Pression en descente (bar)", step=0.01)
        hysteresis = st.number_input("Hystérésis (bar)", step=0.01)
        resultat = st.selectbox("Résultat du test", ["Conforme", "Non conforme"])
    with col2:
        modele = st.text_input("Désignation Modèle")
        visuel = st.selectbox("État visuel", ["OK", "Défaut"])
        fuite = st.selectbox("Fuite détectée", ["Non", "Oui"])
        stabilite = st.selectbox("Stabilité sur 5 cycles", ["Stable", "Instable"])
        prochain = st.date_input("Prochain test (si applicable)")
        val_hysteresis = st.selectbox("Valeur Hystérésis", ["Conforme", "Non conforme"])
        commentaires = st.text_input("Commentaires")

    submit = st.form_submit_button("✅ Enregistrer")

    if submit:
        new_data = {
            "Numéro Pressostat": id,
            "Modèle": modele,
            "Date": str(date),
            "Testé par": testeur,
            "Pression en montée (bar)": declenchement,
            "Pression en descente (bar)": retour,
            "Hystérésis": hysteresis,
            "Valeur Hystérésis": val_hysteresis,
            "Visuel": visuel,
            "Fuite": fuite,
            "Stabilité": stabilite,
            "Prochain test": str(prochain),
            "Résultat": resultat,
            "Commentaires": commentaires
        }

        st.session_state.data.append(new_data)
        df_to_save = pd.DataFrame(st.session_state.data)
        df_to_save.to_csv(csv_file, index=False, sep=';', encoding='utf-8-sig')
        st.success("Test enregistré avec succès.")

# Affichage et gestion
if st.session_state.data:
    df = pd.DataFrame(st.session_state.data)
    st.markdown("### 📋 Tests enregistrés")
    st.markdown("### 🗑 Supprimer un test individuellement")

    for i, row in df.iterrows():
        col1, col2 = st.columns([8, 1])
        with col1:
            st.write(f"**{row['Numéro Pressostat']}** - {row['Date']} - {row['Résultat']}")
        with col2:
            if st.button("🗑", key=f"delete_{i}"):
                st.session_state.data.pop(i)
                df_after = pd.DataFrame(st.session_state.data)
                df_after.to_csv(csv_file, index=False, sep=';', encoding='utf-8-sig')
                st.rerun()

    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False, sep=';', encoding="utf-8-sig").encode("utf-8-sig")
    st.download_button("📥 Télécharger le fichier CSV", csv, "tests_pressostats.csv", "text/csv")

    if st.button("🗑 Effacer tous les tests"):
        st.session_state.data = []
        if os.path.exists(csv_file):
            os.remove(csv_file)
        st.rerun()