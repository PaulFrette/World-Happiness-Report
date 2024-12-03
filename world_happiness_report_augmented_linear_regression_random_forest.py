# -*- coding: utf-8 -*-
"""World_Happiness_report_augmented_Linear_Regression_Random_Forest

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1zkYVELAi_UBziEsrhBUKERqEznoeKI9W

•	Country name ⇨ Nom du pays concerné par les données.

  •	Year ⇨ Année correspondant à la collecte des données ou à leur extrapolation.

  •	Life Ladder ⇨ Indicateur de bien-être subjectif basé sur les réponses à la question Cantril life ladder, représentant l’évaluation personnelle de la vie sur une échelle de 0 (pire vie possible) à 10 (meilleure vie possible).

  •	Log GDP per capita ⇨ Logarithme naturel du PIB par habitant, mesuré en parité de pouvoir d’achat (PPA) avec des prix constants de 2017.

  •	Social support ⇨ Moyenne nationale des réponses affirmatives à la question sur la possibilité de compter sur des proches en cas de besoin.

  •	Healthy life expectancy at birth ⇨ Espérance de vie en bonne santé à la naissance, estimée à partir des données de l’OMS, interpolées et extrapolées si nécessaire.

  •	Freedom to make life choices ⇨ Moyenne nationale des réponses à la question sur la satisfaction vis-à-vis de la liberté de choix dans sa vie.

  •	Generosity ⇨ Résiduel de la régression de la réponse à la question sur les dons aux œuvres de charité au cours du dernier mois sur le PIB par habitant.

  •	Perceptions of corruption ⇨ Moyenne nationale des perceptions de la corruption dans les gouvernements et les entreprises, basée sur les réponses aux enquêtes du Gallup World Poll.

  •	Positive affect ⇨ Moyenne des indicateurs positifs comme le rire, le plaisir et les activités intéressantes vécues pendant une journée typique.

  •	Negative affect ⇨ Moyenne des indicateurs négatifs comme l’inquiétude, la tristesse et la colère vécues pendant une journée typique.
"""

import pandas as pd
import plotly.express as px

df = pd.read_csv("/content/Data_Happiness.csv")
df.info()
df.describe()

"""## Fill Missing values by filtering by country and using bfill or other"""

df_clean = df.dropna()
df_clean["Country name"].nunique()
df_clean.info()

#HeatMap de Correlation

import seaborn as sns

sns.heatmap(df_clean[['Life Ladder', 'Log GDP per capita',
       'Social support', 'Healthy life expectancy at birth',
       'Freedom to make life choices', 'Generosity',
       'Perceptions of corruption', 'Positive affect', 'Negative affect']].corr(), annot=True)

df_clean[['region', 'sub-region', 'Category']].nunique()

df_clean.columns

X = df_clean.drop(columns=["Life Ladder","Country name", 'year'])
y = df_clean['Life Ladder']

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y)

X_train_num = X_train.drop(columns=['region', 'sub-region', 'Category'])
X_test_num = X_test.drop(columns=['region', 'sub-region', 'Category'])

X_train_cat = X_train[['region', 'sub-region', 'Category']]
X_test_cat = X_test[['region', 'sub-region', 'Category']]

from sklearn.preprocessing import OneHotEncoder

ohe = OneHotEncoder(sparse_output=False)
ohe_values_train_X_train_cat = ohe.fit_transform(X_train_cat)
ohe_values_X_test_cat = ohe.transform(X_test_cat)

ohe_values_train_X_train_cat = pd.DataFrame(ohe_values_train_X_train_cat, columns=ohe.get_feature_names_out())
ohe_values_X_test_cat = pd.DataFrame(ohe_values_X_test_cat, columns=ohe.get_feature_names_out())



from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_train_num_scaled = scaler.fit_transform(X_train_num)
X_test_num_scaled = scaler.transform(X_test_num)

X_train_num_scaled = pd.DataFrame(X_train_num_scaled, columns=X_train_num.columns)
X_test_num_scaled = pd.DataFrame(X_test_num_scaled, columns=X_test_num.columns)

import pandas as pd

X_train_final = pd.concat([X_train_num_scaled, ohe_values_train_X_train_cat], axis=1)
X_test_final = pd.concat([X_test_num_scaled, ohe_values_X_test_cat], axis=1)

X_test_final

from sklearn.linear_model import LinearRegression

model = LinearRegression()
model.fit(X_train_final,y_train)

model.score(X_test_final,y_test)



import matplotlib.pyplot as plt
coefficients = model.coef_
feature_names = X_train_final.columns
feature_names
plt.bar(feature_names, coefficients)
plt.xticks(rotation=90)
plt.show()



"""### Random Forest"""

from sklearn.ensemble import RandomForestRegressor  # Ou RandomForestClassifier
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
clf = rf_model.fit(X_test_final, y_test)

clf.score(X_test_final, y_test)

importance = clf.feature_importances_



"""Tracer les coefficients de la regression lineaire"""