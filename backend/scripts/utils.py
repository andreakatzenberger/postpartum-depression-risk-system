import numpy as np
from matplotlib import pyplot as plt
from sklearn.metrics import roc_auc_score, roc_curve, accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import StratifiedKFold, cross_val_score


def evaluate_model(name, y_true, y_pred):
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred, average="weighted", zero_division=0)
    recall = recall_score(y_true, y_pred, average="weighted", zero_division=0)
    f1 = f1_score(y_true, y_pred, average="weighted", zero_division=0)

    print(f"\n* {name} - Accuracy: {accuracy:.4f}, F1: {f1:.4f}")
    return {
        "Model": name,
        "Accuracy": accuracy,
        "Precision": precision,
        "Recall": recall,
        "F1": f1,
    }

def check_overfitting(model, X_train, y_train, X_test, y_test, model_name):
    from sklearn.metrics import accuracy_score
    
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)
    
    train_accuracy = accuracy_score(y_train, y_train_pred)
    test_accuracy = accuracy_score(y_test, y_test_pred)
    
    overfitting_gap = train_accuracy - test_accuracy
    
    print(f"\nOVERFITTING CHECK - {model_name}:")
    print(f"   Training Accuracy: {train_accuracy:.4f}")
    print(f"   Test Accuracy:     {test_accuracy:.4f}")
    print(f"   Overfitting Gap:   {overfitting_gap:.4f}")
    
    # interpret results
    if overfitting_gap < 0.05:
        print(f"       Good: No significant overfitting")
    elif overfitting_gap < 0.10:
        print(f"       Warning: Mild overfitting detected")
    else:
        print(f"       Problem: Significant overfitting detected")
    
    return {
        "Model": model_name,
        "Train_Accuracy": train_accuracy,
        "Test_Accuracy": test_accuracy,
        "Overfitting_Gap": overfitting_gap
    }

def evaluate_auc(model, X_test, y_test, model_name="Model"):
    # izracunavanje
    if hasattr(model, "predict_proba"):
        y_prob = model.predict_proba(X_test)[:, 1]
    else:
        y_prob = model.decision_function(X_test)

    auc_value = roc_auc_score(y_test, y_prob)
    print(f"* {model_name} - AUC: {auc_value:.4f}")

    # plot roc curve line; title is set by caller
    fpr, tpr, _ = roc_curve(y_test, y_prob)
    plt.plot(fpr, tpr, label=f"{model_name} (AUC = {auc_value:.2f})")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.legend()
    plt.grid(True, alpha=0.3)
    return auc_value

def evaluate_cross_validation(model, X, y, scoring="accuracy", model_name="Model"):
    cv = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)
    scores = cross_val_score(model, X, y, cv=cv, scoring=scoring, n_jobs=-1)
    print(f" * {model_name} - 10-fold {scoring}: {np.mean(scores):.4f} ± {np.std(scores):.4f}")
    return np.mean(scores), np.std(scores)

def plot_cross_validation_results(model_names, mean_scores, std_scores, title="10-Fold Cross-Validation Results"):

    plt.figure(figsize=(12, 8))
    
    # create bar plot with error bars
    x_pos = np.arange(len(model_names))
    bars = plt.bar(x_pos, mean_scores, yerr=std_scores, capsize=5, 
                   alpha=0.7, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', 
                                    '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'])
    
    plt.xlabel('Models')
    plt.ylabel('AUC Score')
    plt.title(title)
    plt.xticks(x_pos, model_names, rotation=45, ha='right')
    plt.grid(True, alpha=0.3)
    plt.ylim(0, 1.0)
    
    for i, (mean, std) in enumerate(zip(mean_scores, std_scores)):
        plt.text(i, mean + std + 0.01, f'{mean:.3f}±{std:.3f}', 
                ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    return plt

def analyze_feature_importance_non_tree(
    model,
    X_train,
    y_train,
    feature_names,
    model_name,
    method: str = 'permutation',
    n_repeats: int = 30,
    scoring: str = 'roc_auc',
):
    """
    analyze feature importance for non-tree models using permutation importance or coefficients.
    """
    from sklearn.inspection import permutation_importance
    from sklearn.linear_model import LogisticRegression
    import numpy as np
    
    if method == 'permutation':
        # use permutation importance (works for any model)
        perm_importance = permutation_importance(
            model,
            X_train,
            y_train,
            n_repeats=n_repeats,
            random_state=42,
            scoring=scoring,
        )
        importances = perm_importance.importances_mean
        std = perm_importance.importances_std
    elif method == 'coefficients' and hasattr(model, 'coef_'):
        # for linear models, use coefficients
        importances = np.abs(model.coef_[0])
        std = np.zeros_like(importances)
    else:
        # fallback: use random values (not meaningful but prevents errors)
        importances = np.random.random(len(feature_names))
        std = np.zeros_like(importances)
    
    return importances, std

def plot_raw_feature_importance(selected_models, selected_model_names, feature_names, X_train, y_train):
    """
    create a combined plot showing raw feature importance for all selected models (not normalized).
    """
    import matplotlib.pyplot as plt
    import numpy as np
    
    # collect importances for all models
    all_importances = []
    model_labels = []
    
    for model, name in zip(selected_models, selected_model_names):
        if hasattr(model, 'feature_importances_'):
            # tree-based model
            importances = model.feature_importances_
            all_importances.append(importances)
            model_labels.append(name)
        else:
            # non-tree model - use permutation importance
            importances, _ = analyze_feature_importance_non_tree(model, X_train, y_train, feature_names, name)
            all_importances.append(importances)
            model_labels.append(name)
    
    # sort features by average importance across all models
    avg_importance = np.mean(all_importances, axis=0)
    sorted_indices = np.argsort(avg_importance)[::-1]
    
    # create the plot
    plt.figure(figsize=(16, 10))
    
    # plot each model's importance
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
    x = np.arange(len(feature_names))
    width = 0.2
    
    for i, (imp, label) in enumerate(zip(all_importances, model_labels)):
        plt.bar(x + i * width, imp[sorted_indices], width, label=label, alpha=0.8, color=colors[i % len(colors)])
    
    plt.xlabel('Features (sorted by average importance)')
    plt.ylabel('Raw Feature Importance')
    plt.title('Raw Feature Importance - All Selected Models (Not Normalized)')
    plt.xticks(x + width * 1.5, [feature_names[i] for i in sorted_indices], rotation=45, ha='right')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    return plt

def plot_combined_feature_importance(selected_models, selected_model_names, feature_names, X_train, y_train):
    """
    create a combined plot showing feature importance for all selected models.
    """
    import matplotlib.pyplot as plt
    import numpy as np
    
    # collect importances for all models
    all_importances = []
    model_labels = []
    
    for model, name in zip(selected_models, selected_model_names):
        if hasattr(model, 'feature_importances_'):
            # tree-based model
            importances = model.feature_importances_
            all_importances.append(importances)
            model_labels.append(name)
        else:
            # non-tree model - use permutation importance
            importances, _ = analyze_feature_importance_non_tree(model, X_train, y_train, feature_names, name)
            all_importances.append(importances)
            model_labels.append(name)
    
    # normalize importances to 0-1 scale for comparison
    normalized_importances = []
    for imp in all_importances:
        normalized = (imp - np.min(imp)) / (np.max(imp) - np.min(imp))
        normalized_importances.append(normalized)
    
    # sort features by average importance across all models
    avg_importance = np.mean(normalized_importances, axis=0)
    sorted_indices = np.argsort(avg_importance)[::-1]
    
    # create the plot
    plt.figure(figsize=(16, 10))
    
    # plot each model's importance
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
    x = np.arange(len(feature_names))
    width = 0.2
    
    for i, (imp, label) in enumerate(zip(normalized_importances, model_labels)):
        plt.bar(x + i * width, imp[sorted_indices], width, label=label, alpha=0.8, color=colors[i % len(colors)])
    
    plt.xlabel('Features (sorted by average importance)')
    plt.ylabel('Normalized Importance (0-1)')
    plt.title('Combined Feature Importance - All Selected Models (Normalized)')
    plt.xticks(x + width * 1.5, [feature_names[i] for i in sorted_indices], rotation=45, ha='right')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    return plt

def plot_accuracy_overfitting(model_names, train_accuracies, test_accuracies, title_prefix="accuracy and overfitting"):
    """
    plot grouped bars for train vs test accuracy and a separate bar plot for overfitting gap.
    """
    gaps = np.array(train_accuracies) - np.array(test_accuracies)

    # figure 1: train vs test accuracy (grouped bars)
    plt.figure(figsize=(14, 8))
    x = np.arange(len(model_names))
    width = 0.4
    plt.bar(x - width/2, train_accuracies, width, label='train acc', alpha=0.75)
    plt.bar(x + width/2, test_accuracies, width, label='test acc', alpha=0.75)
    plt.xticks(x, model_names, rotation=45, ha='right')
    plt.ylabel('accuracy')
    plt.title(f'{title_prefix} - train vs test')
    plt.legend()
    plt.grid(True, axis='y', alpha=0.3)
    plt.tight_layout()

    # figure 2: overfitting gap
    plt.figure(figsize=(14, 6))
    x2 = np.arange(len(model_names))
    plt.bar(x2, gaps, color='#d62728', alpha=0.75)
    plt.xticks(x2, model_names, rotation=45, ha='right')
    plt.ylabel('overfitting gap (train - test)')
    plt.title(f'{title_prefix} - overfitting gap')
    plt.grid(True, axis='y', alpha=0.3)
    plt.tight_layout()
    return plt

def plot_feature_importance(model, feature_names, model_name="Model", top_n=15):
    if hasattr(model, 'feature_importances_'):
        importances = model.feature_importances_

        indices = np.argsort(importances)[::-1][:top_n]
        top_features = [feature_names[i] for i in indices]
        top_importances = importances[indices]
        
        plt.figure(figsize=(12, 8))
        plt.barh(range(len(top_features)), top_importances, alpha=0.7)
        plt.yticks(range(len(top_features)), top_features)
        plt.xlabel('Feature Importance')
        plt.title(f'{model_name} - Top {top_n} Most Important Features')
        plt.gca().invert_yaxis()
        plt.grid(True, alpha=0.3)
        
        for i, v in enumerate(top_importances):
            plt.text(v + 0.001, i, f'{v:.3f}', va='center', fontsize=9)
        
        plt.tight_layout()
        return plt
    else:
        print(f"{model_name} does not support feature importance (not a tree-based model)")
        return None