import sys
import numpy as np
import pandas as pd
import sklearn
from sklearn.cluster import AffinityPropagation
from sklearn.cluster import SpectralClustering
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier

from sklearn.datasets import load_iris # dataset

from sklearn.ensemble import IsolationForest

if __name__ == "__main__":
    args = sys.argv
    # args=["", "AP"]
    np.random.seed(42)
    X = np.random.rand(100, 2)
    # X = pd.read_csv("/Users/muyeedahmed/Desktop/Gitcode/AD_Attack/Dataset/analcatdata_apnea2.csv")
    if args[1] == "AP":
        clustering = AffinityPropagation().fit(X)
    elif args[1] == "SC":
        clustering = SpectralClustering().fit(X)
    elif args[1] == "KM":
        clustering = KMeans().fit(X)
    elif args[1] == "GM":
        clustering = GaussianMixture().fit(X)
    elif args[1] == "LogReg":
        X, y = load_iris(return_X_y=True)
        clf = LogisticRegression(max_iter=200).fit(X, y)
    elif args[1] == "DT":
        X, y = load_iris(return_X_y=True)
        clf = DecisionTreeClassifier(solver="saga").fit(X, y)
    elif args[1] == "IF":
        clustering = IsolationForest().fit(X)
