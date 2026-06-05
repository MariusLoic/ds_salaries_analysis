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

# Tableau des données
st.subheader("📋 Données brutes")
if st.checkbox("📋 Cliquez ici pour afficher les données brutes"):
   st.dataframe(df.reset_index(drop=True), height="content")

