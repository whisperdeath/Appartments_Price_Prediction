# 🏠 Estimation des prix des appartements au Maroc

Application de valorisation immobilière propulsée par le Machine Learning. Le projet collecte des annonces d'appartements sur [Avito.ma](https://www.avito.ma), entraîne des modèles de prédiction de prix (vente et location), et expose le tout via une application web **Streamlit** (« PropTech Elite »).

---

## 📋 Aperçu

| Étape | Description |
|-------|-------------|
| **Scraping** | Extraction d'annonces d'appartements depuis Avito.ma via Selenium + BeautifulSoup |
| **Nettoyage** | Préparation des données en deux jeux : vente et location |
| **Modélisation** | XGBoost pour la vente, Régression Linéaire pour la location |
| **Déploiement** | Interface web interactive avec Streamlit |

---

## 🗂️ Structure du projet

```
.
├── scraper.py                       # Scraping des annonces Avito.ma (Selenium + BeautifulSoup)
├── model.py                         # Entraînement et sauvegarde des modèles
├── app.py                           # Application web Streamlit (PropTech Elite)
├── cleaned_apartments_sale.csv      # Données nettoyées — annonces de vente (~5 180 lignes)
├── cleaned_apartments_rent.csv      # Données nettoyées — annonces de location (~5 660 lignes)
├── xgboost_sale_model.pkl           # Modèle XGBoost entraîné (vente)
├── linear_regression_rent_model.pkl # Modèle de régression linéaire (location)
├── encoders_sale.pkl                # LabelEncoders (ville, secteur) — vente
├── encoders_rent.pkl                # LabelEncoders (ville, secteur) — location
├── Rapport PYTHON FINAL.docx        # Rapport du projet
├── pythonprojet.odp                 # Présentation
└── ReadMe.txt                       # Notes originales
```

---

## 🔍 Données

Les modèles utilisent les caractéristiques suivantes :

| Colonne | Description |
|---------|-------------|
| `ville` | Ville de l'appartement (encodée) |
| `secteur` | Secteur / quartier (encodé) |
| `surface` | Superficie en m² |
| `chambres` | Nombre de chambres |
| `salledebain` | Nombre de salles de bain |
| `salons` | Nombre de salons |
| `etage` | Étage |
| `prix` | **Cible** — prix de l'annonce (MAD) |
| `prix_m2` | Prix au mètre carré (dérivé) |

---

## 🤖 Modèles

- **Vente** : `XGBRegressor` (`n_estimators=500`, `max_depth=6`, `learning_rate=0.05`, `subsample=0.8`, `colsample_bytree=0.8`)
- **Location** : `LinearRegression`

Les variables catégorielles (`ville`, `secteur`) sont encodées avec `LabelEncoder`, puis les modèles et encodeurs sont sérialisés avec `joblib`. Les métriques d'évaluation (RMSE, MAE, R²) sont affichées à l'entraînement.

---

## ⚙️ Installation

```bash
git clone https://github.com/whisperdeath/Appartments_Price_Prediction.git
cd Appartments_Price_Prediction

python -m venv venv
source venv/bin/activate        # Windows : venv\Scripts\activate

pip install streamlit pandas numpy scikit-learn xgboost joblib \
            selenium webdriver-manager beautifulsoup4
```

---

## 🚀 Utilisation

**Lancer l'application web :**
```bash
streamlit run app.py
```
Choisissez le mode marché (**Sale** / **Rent**), renseignez la ville, le secteur, la surface et les caractéristiques, puis cliquez sur **GENERATE AI VALUATION** pour obtenir le prix estimé et le prix au m².

**Réentraîner les modèles :**
```bash
python model.py
```

**Relancer le scraping** (nécessite Microsoft Edge) :
```bash
python scraper.py
```

---

## 🛠️ Technologies

`Python` · `Streamlit` · `scikit-learn` · `XGBoost` · `Pandas` · `NumPy` · `Selenium` · `BeautifulSoup` · `joblib`

---

## 👥 Équipe

- **Malak Boussetta** — M1, Master d'Excellence en Intelligence Artificielle
- **Marwa Bouzaouit** — M1, Master d'Excellence en Intelligence Artificielle
- **Aya Adadi** — M1, Master d'Excellence en Intelligence Artificielle
- **Nora Idouaouzal** — M1, Master Big Data & Data Science
- **Sara Ibourk** — M1, Master Big Data & Data Science

---

## ⚠️ Remarque

Le scraping est fourni à des fins pédagogiques. Respectez les conditions d'utilisation d'Avito.ma et les réglementations en vigueur sur la collecte de données.
