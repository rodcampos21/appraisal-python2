import pandas as pd


def select_database_sk(base='a'):
    from sklearn.datasets import load_iris ,load_diabetes,load_breast_cancer
    if base == 'c':
        # c.Pima Indians Diabetes   (https: // www.kaggle.com / datasets / uciml / pima-indians-diabetes-database).
        dataset = load_diabetes()

    elif base == 'b':
        # b.Breast Cancer Wisconsin DataSet (https: // www.kaggle.com / datasets / uciml / breast-cancer-wisconsin-data)
        dataset = load_breast_cancer()
    else:
        # a.Iris Dataset(https: // archive.ics.uci.edu / ml / datasets / iris),
        dataset = load_iris()
    y = dataset.target
    x=  dataset.data
    return dataset,x,y

def select_database(base='a'):
    import pandas as pd
    if base == 'c':
         # c.Pima Indians Diabetes   (https: // www.kaggle.com / datasets / uciml / pima-indians-diabetes-database).
        dataset = pd.read_csv('bases/diabetes.csv')
    elif base=='b':
        # b.Breast Cancer Wisconsin DataSet (https: // www.kaggle.com / datasets / uciml / breast-cancer-wisconsin-data)
        dataset =pd.read_csv('bases/breast.csv')
    else:
        # a.Iris Dataset(https: // archive.ics.uci.edu / ml / datasets / iris),
        dataset = pd.read_csv('bases/iris.csv')
    return dataset

def imputation(x,method=1):
    import numpy as np
    from sklearn.impute import KNNImputer
    if method == 1:
        imputer = KNNImputer(n_neighbors=2)
        data_inputed=pd.DataFrame(imputer.fit_transform(x), columns=["sepal.length","sepal.width","petal.length","petal.width"])
    return data_inputed
#     else method== 2:

def clustering(x,clusters=3,method='1'):

    # if method == 1:
        from sklearn.cluster import KMeans
        model = KMeans(n_clusters=clusters, random_state=0, init = 'k-means++', max_iter = 300, n_init = 10)
        model.fit(x)
        y_pred = model.fit_predict(x)
        data_clustered = pd.DataFrame(model.fit_transform(x))

    # elif method == 2:
    #     x=x[:, [2,3]]
    #     from sklearn.cluster import DBSCAN
    #     model = DBSCAN(eps=0.3, min_samples=10).fit(x)
    #     y_pred = model.fit_predict(x)
        return (y_pred,model,data_clustered)

def plot_clustering(x,y_preds):
    import matplotlib.pyplot as plt
    plt.scatter(x[y_preds == 0, 0], x[y_preds == 0, 1], s=100, c='purple', label='Iris-setosa')
    plt.scatter(x[y_preds == 1, 0], x[y_preds == 1, 1], s=100, c='orange', label='Iris-versicolour')
    plt.scatter(x[y_preds == 2, 0], x[y_preds == 2, 1], s=100, c='green', label='Iris-virginica')
    # # Plotting the centroids of the clusters
    # plt.scatter(model.cluster_centers_[:, 0], model.cluster_centers_[:, 1], s=100, c='red', label='Centroids')
    plt.legend()

def plot_original_iris(X, Y):
     import matplotlib.pyplot as plt
     # plt.subplot(1, 2, 1)
     plt.scatter(X[Y == 0, 0], X[Y == 0, 1], c='red', marker="^", s=50)
     plt.scatter(X[Y == 1, 0], X[Y == 1, 1], c='green', marker="^", s=50)
     plt.scatter(X[Y == 2, 0], X[Y == 2, 1], c='blue', marker="^", s=50)
     plt.title("Original Data")


# Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#   dataset,x,y = select_database_sk('b')
#   y_pred,model = clustering(x, method=2,clusters=3)
#   plot_clustering(x,y_pred)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
