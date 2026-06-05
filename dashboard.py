import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuration
st.set_page_config(page_title="Analyse Salaires Data Science", layout="wide")

# Titre
st.title("📊 Analyse des Salaires en Data Science")
st.markdown("**Auteur : Marius Loïc** | Certifications DataCamp")

# Chargement des données
df = pd.read_csv("data/ds_salaries.csv")

# Sidebar filtres
st.sidebar.header("Filtres")
annee = st.sidebar.multiselect("Année", df['work_year'].unique(), default=df['work_year'].unique())
df = df[df['work_year'].isin(annee)]

# Filtre niveau d'expérience
exp_labels = {'EN': 'Junior', 'MI': 'Mid-level', 'SE': 'Senior', 'EX': 'Executive'}
exp_options = ['Junior', 'Mid-level', 'Senior', 'Executive']
exp_choix = st.sidebar.multiselect("Niveau d'expérience", exp_options, default=exp_options)
exp_codes = [k for k, v in exp_labels.items() if v in exp_choix]
df = df[df['experience_level'].isin(exp_codes)]

# Filtre taille entreprise
taille_labels = {'S': 'Petite', 'M': 'Moyenne', 'L': 'Grande'}
taille_options = ['Petite', 'Moyenne', 'Grande']
taille_choix = st.sidebar.multiselect("Taille entreprise", taille_options, default=taille_options)
taille_codes = [k for k, v in taille_labels.items() if v in taille_choix]
df = df[df['company_size'].isin(taille_codes)]

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Total offres", len(df))
col2.metric("Salaire moyen", f"${df['salary_in_usd'].mean():,.0f}")
col3.metric("Pays représentés", df['company_location'].nunique())

# Graphique 1
st.subheader("Top 10 pays qui recrutent le plus")
top_pays = df['company_location'].value_counts().head(10)
fig, ax = plt.subplots()
sns.barplot(x=top_pays.values, y=top_pays.index, palette='viridis', ax=ax)
st.pyplot(fig)

# Graphique 2
st.subheader("Top 10 postes les plus demandés")
top_postes = df['job_title'].value_counts().head(10)
fig2, ax2 = plt.subplots()
sns.barplot(x=top_postes.values, y=top_postes.index, palette='magma', ax=ax2)
st.pyplot(fig2)

# Graphique 3 : Salaire par niveau d'expérience
st.subheader("Salaire par niveau d'expérience")
fig3, ax3 = plt.subplots()
exp_order = ['EN', 'MI', 'SE', 'EX']
sns.boxplot(data=df, x='experience_level', y='salary_in_usd', order=exp_order, palette='coolwarm', ax=ax3)
ax3.set_xlabel("Niveau")
ax3.set_ylabel("Salaire (USD)")
st.pyplot(fig3)

# Graphique 4 : Salaire moyen par pays
st.subheader("Salaire moyen par pays (Top 10)")
sal_pays = df.groupby('company_location')['salary_in_usd'].mean().sort_values(ascending=False).head(10)
fig4, ax4 = plt.subplots()
sns.barplot(x=sal_pays.values, y=sal_pays.index, palette='Blues_r', ax=ax4)
ax4.set_xlabel("Salaire moyen (USD)")
st.pyplot(fig4)

# Graphique 5 : Salaire moyen par poste
st.subheader("Salaire moyen par poste (Top 10)")
sal_poste = df.groupby('job_title')['salary_in_usd'].mean().sort_values(ascending=False).head(10)
fig5, ax5 = plt.subplots()
sns.barplot(x=sal_poste.values, y=sal_poste.index, palette='Oranges_r', ax=ax5)
ax5.set_xlabel("Salaire moyen (USD)")
st.pyplot(fig5)

# Graphique 6 : Evolution des salaires
st.subheader("📈 Evolution du salaire moyen (2020-2022)")
evolution = df.groupby('work_year')['salary_in_usd'].mean()
fig6, ax6 = plt.subplots()
ax6.plot(evolution.index, evolution.values, marker='o', color='royalblue', linewidth=2)
ax6.set_xlabel("Année")
ax6.set_ylabel("Salaire moyen (USD)")
ax6.set_xticks([2020, 2021, 2022])
ax6.set_xticklabels(['2020', '2021', '2022'])
for x, y in zip(evolution.index, evolution.values):
    ax6.annotate(f"${y:,.0f}", (x, y), textcoords="offset points", xytext=(15,10), ha='left')
st.pyplot(fig6)

# Carte du monde
import plotly.express as px
import pycountry

st.subheader("🗺️ Carte des recrutements par pays")

def convert_alpha2_to_alpha3(code):
    try:
        return pycountry.countries.get(alpha_2=code).alpha_3
    except:
        return None

carte_data = df.groupby('company_location').agg(
    offres=('job_title', 'count'),
    salaire_moyen=('salary_in_usd', 'mean')
).reset_index()

carte_data['iso3'] = carte_data['company_location'].apply(convert_alpha2_to_alpha3)
carte_data = carte_data.dropna(subset=['iso3'])

fig_carte = px.choropleth(
    carte_data,
    locations='iso3',
    locationmode='ISO-3',
    color='offres',
    hover_name='company_location',
    color_continuous_scale='Viridis',
    title="Nombre d'offres par pays"
)
st.plotly_chart(fig_carte, use_container_width=True)

# Prédicteur de salaire
st.subheader("🤖 Estimation de salaire")
st.caption("📌 Estimation basée sur les données historiques 2020-2022. Les salaires réels peuvent varier.")

col1, col2, col3 = st.columns(3)

with col1:
    poste_choix = st.selectbox("Poste", sorted(df['job_title'].unique()))

with col2:
    exp_choix_pred = st.selectbox("Niveau d'expérience", 
    ['Junior (EN)', 'Mid-level (MI)', 'Senior (SE)', 'Executive (EX)'])

with col3:
    pays_choix = st.selectbox("Pays", sorted(df['company_location'].unique()))

exp_map = {'Junior (EN)': 'EN', 'Mid-level (MI)': 'MI', 'Senior (SE)': 'SE', 'Executive (EX)': 'EX'}
exp_code = exp_map[exp_choix_pred]

filtre = df[
    (df['job_title'] == poste_choix) & 
    (df['experience_level'] == exp_code) & 
    (df['company_location'] == pays_choix)
]

st.markdown("---")

if len(filtre) > 0:
    salaire_pred = filtre['salary_in_usd'].mean()
    st.success(f"💰 Salaire estimé : **${salaire_pred:,.0f} / an**")
    st.info(f"Basé sur {len(filtre)} offre(s) similaire(s)")
else:
    salaire_global = df[df['job_title'] == poste_choix]['salary_in_usd'].mean()
    if not pd.isna(salaire_global):
        nb_offres = len(df[df['job_title'] == poste_choix])
        st.success(f"💰 Salaire estimé : **${salaire_global:,.0f} / an**")
        st.info(f"Basé sur {nb_offres} offre(s) similaire(s) dans le monde")
    else:
        st.error("❌ Aucune donnée disponible pour cette combinaison.")

# Comparaison Afrique vs Monde
st.subheader("🌍 Afrique vs Monde")

pays_afrique = ['NG', 'EG', 'KE', 'ZA', 'TN', 'DZ', 'CM', 'GH', 'SN']

sal_afrique = df[df['company_location'].isin(pays_afrique)]['salary_in_usd'].mean()
sal_monde = df[~df['company_location'].isin(pays_afrique)]['salary_in_usd'].mean()

col1, col2 = st.columns(2)
col1.metric("💰 Salaire moyen Afrique", f"${sal_afrique:,.0f}" if not pd.isna(sal_afrique) else "Pas de données")
col2.metric("💰 Salaire moyen Monde", f"${sal_monde:,.0f}")

offres_afrique = len(df[df['company_location'].isin(pays_afrique)])
offres_monde = len(df[~df['company_location'].isin(pays_afrique)])

fig7, ax7 = plt.subplots()
ax7.bar(['Afrique', 'Reste du Monde'], [offres_afrique, offres_monde], color=['#FF6B35', '#4ECDC4'])
ax7.set_ylabel("Nombre d'offres")
ax7.set_title("Nombre d'offres : Afrique vs Monde")
st.pyplot(fig7)

# Tableau des données
st.subheader("📋 Données brutes")
if st.checkbox("📋 Cliquez ici pour afficher les données brutes"):
   st.dataframe(df.reset_index(drop=True), height="content")

