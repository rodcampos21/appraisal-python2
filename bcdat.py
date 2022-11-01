##  instalar E IMPORTAR AS BBL (pandas)
##  LER O CSV  com pandas
##  Separar em train e test 80/20
##  Chamar a função do KNN ( da uma lida do que se trata KNN)
##  ANÁLISE DE ACURÁCIA expected 10%

import pandas as pd
## falou CSV importar o pandas
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Substitua o "C:\Users\usuario\Desktop\dados.csv" pelo caminho e nome do seu arquivo

df = pd.read_csv("C:/Users/Rodrigo/PycharmProjects/appraisal-python/KNN/data.csv")
# dropping 'Unnamed: 32' column.
df.drop("Unnamed: 32", axis=1, inplace=True)
# dropping id column
df.drop('id',axis=1, inplace=True)

train,test = train_test_split(df, test_size=0.2, random_state=42)

neigh = KNeighborsClassifier(n_neighbors=5)
features=train.drop("diagnosis",axis=1, inplace=False)
neigh.fit(features, train.diagnosis)

features_test=test.drop("diagnosis",axis=1, inplace=False)
resposta_neigh=neigh.predict(features_test)
acuracia=accuracy_score(test.diagnosis,resposta_neigh)

print("Acurácia do KNN: ", (acuracia*100), "%")


