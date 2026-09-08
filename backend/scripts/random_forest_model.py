from sklearn.ensemble import RandomForestClassifier
from scripts.utils import evaluate_model

def train_random_forest(X_train, X_test, y_train, y_test, n_estimators=100, max_depth=None, min_samples_split=2, min_samples_leaf=1, max_features='sqrt', bootstrap=True, random_state=42):
    """
    - n_estimators: int (number of trees)
    - max_depth: int or None (max tree depth)
    - min_samples_split: int (min samples to split)
    - min_samples_leaf: int (min samples per leaf)
    - max_features: 'sqrt', 'log2', int, float, or None
    - bootstrap: bool (use bootstrap sampling)
    """
    model = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        min_samples_split=min_samples_split,
        min_samples_leaf=min_samples_leaf,
        max_features=max_features,
        bootstrap=bootstrap,
        random_state=random_state
    )
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    results = evaluate_model(f"Random Forest (n_est={n_estimators}, max_depth={max_depth})", y_test, y_pred)
    return results, model