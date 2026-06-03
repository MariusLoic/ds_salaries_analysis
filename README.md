# Data Science Salaries — Analyse mondiale 

Analyse exploratoire des salaires dans la Data Science à l'échelle mondiale, basée sur le dataset **ds_salaries.csv** (607 entrées, 2020–2022).

## Questions analysées

| # | Question | Réponse clé |
|---|----------|-------------|
| 1 | Quels pays recrutent le plus ? | 🇺🇸 USA (58.5%) · 🇬🇧 UK · 🇨🇦 Canada |
| 2 | Quels postes sont les plus demandés ? | Data Scientist · Data Engineer · Data Analyst |
| 3 | Quels salaires sont les mieux payés ? | Data Analytics Lead : **$405 000** / an |

## Structure du projet

```
ds_salaries_project/
├── analysis.py          # Script principal (analyse + graphiques)
├── ds_salaries.csv      # Dataset source
├── salaire_experience.png  # Graphiques générés
├── salaire_pays.png  # Graphiques générés
├── salaire_poste.png  # Graphiques générés
├── top_pays.png  # Graphiques générés
├── top_postes.png  # Graphiques générés
└── README.md
```

## Installation & exécution

```bash
# Cloner le repo
git clone https://github.com/TON_USERNAME/ds-salaries-analysis.git
cd ds-salaries-analysis

# Installer les dépendances
pip install pandas matplotlib

# Lancer l'analyse
python analysis.py
```

## Résultats clés

###  Recrutement par pays
- **58.5%** des offres viennent des États-Unis (355/607)
- UK, Canada, Allemagne et Inde complètent le Top 5
- Le marché est **très concentré** : 3 pays = 71% des offres

###  Postes les plus demandés
1. **Data Scientist** — 143 offres
2. **Data Engineer** — 132 offres
3. **Data Analyst** — 97 offres
4. **ML Engineer** — 41 offres

###  Salaires (en USD)
| Poste | Salaire moyen |
|-------|--------------|
| Data Analytics Lead | $405 000 |
| Principal Data Engineer | $328 333 |
| Principal Data Scientist | $215 242 |
| Data Engineer | ~$140 000 |
| Data Analyst | ~$100 000 |

| Niveau | Salaire moyen |
|--------|--------------|
| Executive | $199 392 |
| Senior | $138 617 |
| Mid-level | $87 996 |
| Entry-level | $61 643 |

###  Remote & tendances
- **62.8%** des postes sont 100% en télétravail
- Salaire moyen en hausse de **+30%** entre 2020 et 2022

## Graphiques générés

Le script produit **5 graphiques**  :
1. Top 10 pays recruteurs
2. Top 10 postes les plus demandés
3. Salaire moyen par poste (top 10)
4. Salaire moyen par pays (top 10)
5. Salaire moyen par niveau d'expérience

## Technologies utilisées

- **Python 3.14.5**
- **pandas** — manipulation des données
- **matplotlib** — visualisations

---

*Dataset source : [ds_salaries sur Kaggle](https://www.kaggle.com/datasets/ruchi798/data-science-job-salaries)*


# Auteur

**Marius Loïc**
- GitHub : [MariusLoic](https://github.com/MariusLoic)
- Certifications : Data Engineering Associate | Data Analyst Associate
- ngninmeum@gmail.com