from sklearn.neighbors import KNeighborsClassifier
from scripts.utils import evaluate_model

def train_knn(X_train, X_test, y_train, y_test, n_neighbors=5, weights='uniform', algorithm='auto', leaf_size=30, p=2, metric='minkowski'):
    """
    - n_neighbors: int (number of neighbors)
    - weights: 'uniform' or 'distance'
    - algorithm: 'auto', 'ball_tree', 'kd_tree', 'brute'
    - metric: 'minkowski', 'euclidean', 'manhattan', etc.
    """
    model = KNeighborsClassifier(
        n_neighbors=n_neighbors,
        weights=weights,
        algorithm=algorithm,
        leaf_size=leaf_size,
        p=p,
        metric=metric
    )
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    results = evaluate_model(f"KNN (k={n_neighbors}, weights={weights})", y_test, y_pred)
    return results, model