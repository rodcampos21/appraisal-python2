import pandas as pd
from main import  imputation, clustering
import os


def comparacao_imputação(original_dataset_name,column):
    appraisal_eraser(original_dataset_name, column)
    appraisal_crowner( column)
    print("Resultado com Appraisal")
    appraisal_reviewer(original_dataset_name,"dataset_filled.csv ", column)
    imputacao_simples("dataset_missing.csv")
    print("Resultado com Imputação KNN")
    appraisal_reviewer(original_dataset_name,"dataset_filled_imputation.csv", column)

def appraisal_eraser(name,column):
    comando='python eraser.py -i '+ name +' -o dataset_missing.csv -m MCAR -a ' + column + ' -r .3 '
    os.system('cmd /c '+ comando)

def imputacao_simples(filename_in):
    missing_dataset = pd.read_csv(filename_in)
    try:
        missing_dataset=missing_dataset.drop(['variety'], axis=1)
    finally:
        resultado =imputation(missing_dataset)
        resultado.to_csv('dataset_filled_imputation.csv')

def agrupamento(filename_in,filename_out):
    missing_dataset = pd.read_csv(filename_in)
    try:
        missing_dataset=missing_dataset.drop(['variety'], axis=1)
    finally:
        _,_,resultado =clustering(missing_dataset)
        resultado.to_csv(filename_out)

def appraisal_crowner(column):
    comando='python crowner.py  -i  dataset_missing.csv -o dataset_filled.csv -p mean -a ' + column
    os.system('cmd /c '+ comando)

def appraisal_reviewer(nameoriginal,namefilled,column):
    comando='python reviewer.py -o '+nameoriginal +' -f ' +namefilled+' -m MSE -a ' + column
    os.system('cmd /c '+ comando)


if __name__ == '__main__':

    # appraisal_eraser('iris.csv', "sepal.length")
    # imputacao_simples('dataset_missing.csv')
    # agrupamento("dataset_filled_imputation.csv","dataset_clustered.csv")

    comparacao_imputação('iris.csv', 'sepal.length')


