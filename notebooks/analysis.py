"""
=============================================================
  Data Science Salaries — Analyse mondiale (2020–2022)
  Source : ds_salaries.csv  |  607 entrées
=============================================================
  Questions :
    1. Quels pays recrutent le plus ?
    2. Quels postes sont les plus demandés ?
    3. Quels sont les salaires les mieux payés ?
       → par poste, par pays, par niveau d'expérience
=============================================================
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mticker
import warnings
warnings.filterwarnings("ignore")

# ── Configuration esthétique ──────────────────────────────
PALETTE = {
    "blue":   "#378ADD",
    "green":  "#1D9E75",
    "amber":  "#BA7517",
    "gray":   "#888780",
    "coral":  "#D85A30",
}
BACKGROUND = "#FAFAFA"
TEXT       = "#2C2C2A"
GRID_COLOR = "#E8E6DF"

plt.rcParams.update({
    "font.family":        "DejaVu Sans",
    "axes.facecolor":     BACKGROUND,
    "figure.facecolor":   BACKGROUND,
    "axes.edgecolor":     GRID_COLOR,
    "axes.grid":          True,
    "grid.color":         GRID_COLOR,
    "grid.linewidth":     0.6,
    "text.color":         TEXT,
    "axes.labelcolor":    TEXT,
    "xtick.color":        TEXT,
    "ytick.color":        TEXT,
    "axes.spines.top":    False,
    "axes.spines.right":  False,
})

# ─────────────────────────────────────────────────────────
# 1. CHARGEMENT DES DONNÉES
# ─────────────────────────────────────────────────────────
df = pd.read_csv("data/ds_salaries.csv")

EXP_MAP = {"EN": "Entry-level", "MI": "Mid-level", "SE": "Senior", "EX": "Executive"}
df["exp_label"] = df["experience_level"].map(EXP_MAP)

print("=" * 55)
print("  Dataset chargé")
print(f"  Lignes : {len(df)} | Colonnes : {df.shape[1]}")
print(f"  Années : {sorted(df['work_year'].unique())}")
print(f"  Pays uniques : {df['company_location'].nunique()}")
print(f"  Postes uniques : {df['job_title'].nunique()}")
print("=" * 55)

# ─────────────────────────────────────────────────────────
# 2. CALCULS
# ─────────────────────────────────────────────────────────

# Q1 — Top 10 pays recruteurs
top_countries = (
    df["company_location"]
    .value_counts()
    .head(10)
    .sort_values()
)

# Q2 — Top 10 postes demandés
top_jobs = (
    df["job_title"]
    .value_counts()
    .head(10)
    .sort_values()
)

# Q3a — Salaire moyen par poste (les 10 mieux rémunérés)
salary_by_job = (
    df.groupby("job_title")["salary_in_usd"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
    .sort_values()
)

# Q3b — Salaire moyen par pays (top 10)
salary_by_country = (
    df.groupby("company_location")["salary_in_usd"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
    .sort_values()
)

# Q3c — Salaire moyen par niveau d'expérience
exp_order   = ["Entry-level", "Mid-level", "Senior", "Executive"]
salary_exp  = df.groupby("exp_label")["salary_in_usd"].mean().reindex(exp_order)

# Remote ratio
remote_labels = {0: "Présentiel\n(0%)", 50: "Hybride\n(50%)", 100: "Full remote\n(100%)"}
remote_counts = df["remote_ratio"].value_counts().rename(index=remote_labels)

# Tendance annuelle
trend = df.groupby("work_year")["salary_in_usd"].mean()

# ─────────────────────────────────────────────────────────
# 3. GRAPHIQUES
# ─────────────────────────────────────────────────────────

def add_bar_labels(ax, fmt="{:.0f}", color=TEXT, offset=500):
    for bar in ax.patches:
        w = bar.get_width()
        if w > 0:
            ax.text(
                w + offset,
                bar.get_y() + bar.get_height() / 2,
                fmt.format(w),
                va="center", ha="left",
                fontsize=9, color=color
            )

def fmt_usd(x, _):
    return f"${x/1_000:.0f}K"


fig, axes = plt.subplots(2, 3, figsize=(18, 11))
fig.suptitle("Data Science Salaries — Analyse mondiale (2020–2022)", fontsize=17, fontweight="medium", y=1.01)
axes[1, 2].set_visible(False)   # cellule vide

# ── Graphique 1 : Top 10 pays recruteurs ─────────────────
ax1 = axes[0, 0]
bars = ax1.barh(top_countries.index, top_countries.values, color=PALETTE["blue"], height=0.6)
add_bar_labels(ax1, fmt="{:.0f}", offset=3)
ax1.set_title("Top 10 pays recruteurs", fontsize=13, fontweight="medium", pad=10)
ax1.set_xlabel("Nombre d'offres")
ax1.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))
ax1.set_xlim(0, top_countries.max() * 1.18)

# ── Graphique 2 : Top 10 postes demandés ─────────────────
ax2 = axes[0, 1]
short_labels = [
    t.replace("Machine Learning", "ML")
     .replace("Research ", "Rech. ")
     .replace("Data Science", "DS")
    for t in top_jobs.index
]
ax2.barh(short_labels, top_jobs.values, color=PALETTE["green"], height=0.6)
add_bar_labels(ax2, fmt="{:.0f}", offset=1)
ax2.set_title("Top 10 postes les plus demandés", fontsize=13, fontweight="medium", pad=10)
ax2.set_xlabel("Nombre d'offres")
ax2.set_xlim(0, top_jobs.max() * 1.18)

# ── Graphique 3 : Salaire moyen par poste ────────────────
ax3 = axes[0, 2]
short_job = [
    t.replace("Principal ", "Princ. ")
     .replace("Financial ", "Fin. ")
     .replace("Director of ", "Dir. ")
     .replace("Applied ", "App. ")
     .replace("Analytics ", "Anlt. ")
    for t in salary_by_job.index
]
ax3.barh(short_job, salary_by_job.values, color=PALETTE["amber"], height=0.6)
ax3.xaxis.set_major_formatter(mticker.FuncFormatter(fmt_usd))
for bar in ax3.patches:
    w = bar.get_width()
    ax3.text(w + 3000, bar.get_y() + bar.get_height() / 2,
             f"${w/1000:.0f}K", va="center", ha="left", fontsize=8.5, color=TEXT)
ax3.set_title("Salaire moyen par poste (Top 10)", fontsize=13, fontweight="medium", pad=10)
ax3.set_xlabel("Salaire moyen (USD)")
ax3.set_xlim(0, salary_by_job.max() * 1.22)

# ── Graphique 4 : Salaire par pays ───────────────────────
ax4 = axes[1, 0]
ax4.barh(salary_by_country.index, salary_by_country.values, color=PALETTE["coral"], height=0.6)
ax4.xaxis.set_major_formatter(mticker.FuncFormatter(fmt_usd))
for bar in ax4.patches:
    w = bar.get_width()
    ax4.text(w + 1500, bar.get_y() + bar.get_height() / 2,
             f"${w/1000:.0f}K", va="center", ha="left", fontsize=8.5, color=TEXT)
ax4.set_title("Salaire moyen par pays (Top 10)", fontsize=13, fontweight="medium", pad=10)
ax4.set_xlabel("Salaire moyen (USD)")
ax4.set_xlim(0, salary_by_country.max() * 1.22)

# ── Graphique 5 : Salaire par expérience ─────────────────
ax5 = axes[1, 1]
colors_exp = [PALETTE["blue"], PALETTE["green"], PALETTE["amber"], PALETTE["coral"]]
bars5 = ax5.bar(salary_exp.index, salary_exp.values, color=colors_exp, width=0.55)
ax5.yaxis.set_major_formatter(mticker.FuncFormatter(fmt_usd))
for bar in bars5:
    h = bar.get_height()
    ax5.text(bar.get_x() + bar.get_width() / 2, h + 2500,
             f"${h/1000:.0f}K", ha="center", va="bottom", fontsize=10, fontweight="medium", color=TEXT)
ax5.set_title("Salaire moyen par niveau d'expérience", fontsize=13, fontweight="medium", pad=10)
ax5.set_ylabel("Salaire moyen (USD)")
ax5.set_ylim(0, salary_exp.max() * 1.2)
ax5.tick_params(axis="x", labelsize=10)

plt.tight_layout(pad=2.5)
plt.savefig("ds_salaries_analysis.png", dpi=150, bbox_inches="tight", facecolor=BACKGROUND)
plt.close()
print("\n  Graphique sauvegardé : ds_salaries_analysis.png")

# ─────────────────────────────────────────────────────────
# 4. RÉSUMÉ STATISTIQUE
# ─────────────────────────────────────────────────────────
print("\n" + "=" * 55)
print("  RÉSULTATS CLÉS")
print("=" * 55)

print("\n[Q1] Top 5 pays recruteurs :")
for country, n in top_countries.sort_values(ascending=False).head(5).items():
    pct = n / len(df) * 100
    print(f"  {country:4s} : {n:4d} offres ({pct:.1f}%)")

print("\n[Q2] Top 5 postes demandés :")
for job, n in top_jobs.sort_values(ascending=False).head(5).items():
    print(f"  {job:<30s} : {n:3d} offres")

print("\n[Q3a] Top 5 salaires par poste :")
for job, sal in salary_by_job.sort_values(ascending=False).head(5).items():
    print(f"  {job:<30s} : ${sal:,.0f}")

print("\n[Q3b] Top 5 salaires par pays :")
for country, sal in salary_by_country.sort_values(ascending=False).head(5).items():
    print(f"  {country:4s} : ${sal:,.0f}")

print("\n[Q3c] Salaire par niveau d'expérience :")
for exp, sal in salary_exp.items():
    print(f"  {exp:<15s} : ${sal:,.0f}")

remote_pct = df["remote_ratio"].value_counts(normalize=True) * 100
print("\n[BONUS] Répartition remote :")
for ratio, pct in remote_pct.sort_index(ascending=False).items():
    print(f"  {ratio:3d}% remote : {pct:.1f}%")

print("\n[BONUS] Évolution salaire moyen :")
for year, sal in trend.items():
    print(f"  {year} : ${sal:,.0f}")

print("\n" + "=" * 55)
print("  Analyse terminée avec succès !")
print("=" * 55)


# ============================================
# VISUALISATIONS
# ============================================

# Graphique 1 : Top 10 pays qui recrutent le plus
plt.figure(figsize=(12, 6))
top_pays = df['company_location'].value_counts().head(10)
sns.barplot(x=top_pays.values, y=top_pays.index, palette='viridis')
plt.title('Top 10 pays qui recrutent le plus', fontsize=16)
plt.xlabel('Nombre de recrutements')
plt.ylabel('Pays')
plt.tight_layout()
plt.savefig('top_pays.png')
plt.show()
print("Graphique 1 sauvegardé !")

# Graphique 2 : Top 10 postes les plus demandés
plt.figure(figsize=(12, 6))
top_postes = df['job_title'].value_counts().head(10)
sns.barplot(x=top_postes.values, y=top_postes.index, palette='magma')
plt.title('Top 10 postes les plus demandés', fontsize=16)
plt.xlabel('Nombre d\'offres')
plt.ylabel('Poste')
plt.tight_layout()
plt.savefig('top_postes.png')
plt.show()
print("Graphique 2 sauvegardé !")

# Graphique 3 : Salaire par niveau d'expérience
plt.figure(figsize=(10, 6))
exp_order = ['EN', 'MI', 'SE', 'EX']
sns.boxplot(data=df, x='experience_level', y='salary_in_usd', order=exp_order, palette='coolwarm')
plt.title('Salaire par niveau d\'expérience', fontsize=16)
plt.xlabel('Niveau')
plt.ylabel('Salaire (USD)')
plt.tight_layout()
plt.savefig('salaire_experience.png')
plt.show()
print("Graphique 3 sauvegardé !")

# Graphique 4 : Salaire moyen par pays (Top 10)
plt.figure(figsize=(12, 6))
sal_pays = df.groupby('company_location')['salary_in_usd'].mean().sort_values(ascending=False).head(10)
sns.barplot(x=sal_pays.values, y=sal_pays.index, palette='Blues_r')
plt.title('Salaire moyen par pays (Top 10)', fontsize=16)
plt.xlabel('Salaire moyen (USD)')
plt.ylabel('Pays')
plt.tight_layout()
plt.savefig('salaire_pays.png')
plt.show()
print("Graphique 4 sauvegardé !")

# Graphique 5 : Salaire moyen par poste (Top 10)
plt.figure(figsize=(12, 6))
sal_poste = df.groupby('job_title')['salary_in_usd'].mean().sort_values(ascending=False).head(10)
sns.barplot(x=sal_poste.values, y=sal_poste.index, palette='Oranges_r')
plt.title('Salaire moyen par poste (Top 10)', fontsize=16)
plt.xlabel('Salaire moyen (USD)')
plt.ylabel('Poste')
plt.tight_layout()
plt.savefig('salaire_poste.png')
plt.show()
print("Graphique 5 sauvegardé !")