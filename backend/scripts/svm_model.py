from sklearn.svm import SVC
from scripts.utils import evaluate_model

def train_svm(X_train, X_test, y_train, y_test, kernel='rbf', C=1.0, gamma='scale', degree=3, coef0=0.0, shrinking=True, probability=True, tol=1e-3, cache_size=200, class_weight=None, verbose=False, max_iter=-1, decision_function_shape='ovr', break_ties=False, random_state=42):
    """
    - kernel: 'rbf', 'linear', 'poly', 'sigmoid'
    - C: float (regularization parameter)
    - gamma: 'scale', 'auto', or float (kernel coefficient)
    - degree: int (polynomial kernel degree)
    - probability: bool (enable probability estimates)
    """
    model = SVC(
        kernel=kernel,
        C=C,
        gamma=gamma,
        degree=degree,
        coef0=coef0,
        shrinking=shrinking,
        probability=probability,
        tol=tol,
        cache_size=cache_size,
        class_weight=class_weight,
        verbose=verbose,
        max_iter=max_iter,
        decision_function_shape=decision_function_shape,
        break_ties=break_ties,
        random_state=random_state
    )
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    results = evaluate_model(f"SVM ({kernel}, C={C}, gamma={gamma})", y_test, y_pred)
    return results, model
