import os

import pandas as pd
from matplotlib import pyplot as plt

from scripts.preprocessing import preprocess_data
from scripts.random_forest_model import train_random_forest
from scripts.knn_model import train_knn
from scripts.naive_bayes_model import train_naive_bayes
from scripts.svm_model import train_svm
from scripts.utils import (
    evaluate_auc,
    evaluate_cross_validation,
    check_overfitting,
    plot_feature_importance,
    plot_combined_feature_importance,
)

RESULTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
os.makedirs(RESULTS_DIR, exist_ok=True)

# preprocessing i podela podataka u training i eval skup
train_df, test_df = preprocess_data()

# ciljna promenljiva
target_column = "feeling anxious"
X_train = train_df.drop(columns=[target_column])
y_train = train_df[target_column]
X_test = test_df.drop(columns=[target_column])
y_test = test_df[target_column]
feature_names = X_train.columns.tolist()

# finalni modeli - po jedan konfigurisan set parametara po tipu,
# izabrani na osnovu AUC poredjenja iz eksperimentalne faze
results_rf, rf_model = train_random_forest(
    X_train, X_test, y_train, y_test,
    n_estimators=300, max_depth=20, min_samples_split=3, min_samples_leaf=1, max_features="log2",
)
results_knn, knn_model = train_knn(
    X_train, X_test, y_train, y_test,
    n_neighbors=7, weights="distance", metric="euclidean",
)
results_nb, nb_model = train_naive_bayes(
    X_train, X_test, y_train, y_test,
    model_type="gaussian", var_smoothing=1e-09,
)
results_svm, svm_model = train_svm(
    X_train, X_test, y_train, y_test,
    kernel="rbf", C=100.0, gamma="scale", class_weight="balanced",
)

models = [rf_model, knn_model, nb_model, svm_model]
model_names = ["Random Forest", "KNN", "Naive Bayes", "SVM"]
model_results = [results_rf, results_knn, results_nb, results_svm]

print("\n=== SVI MODELI TRENIRANI ===")
for res in model_results:
    print(f"* {res['Model']} - Accuracy: {res['Accuracy']:.4f}, F1: {res['F1']:.4f}")

# ROC krive i AUC
print("\n=== ROC / AUC ===")
plt.figure(figsize=(10, 8))
auc_scores = {}
for model, name in zip(models, model_names):
    auc_scores[name] = evaluate_auc(model, X_test, y_test, name)
plt.plot([0, 1], [0, 1], "k--", label="nasumično (AUC = 0.5)")
plt.title("ROC krive - finalni modeli")
plt.legend()
plt.savefig(os.path.join(RESULTS_DIR, "roc_curves.png"), bbox_inches="tight")
plt.show()

# 10-fold cross-validation NA TRENING SKUPU (ne na test skupu)
print("\n=== 10-FOLD CROSS-VALIDATION (AUC, trening skup) ===")
cv_scores = {}
for model, name in zip(models, model_names):
    mean_cv, std_cv = evaluate_cross_validation(model, X_train, y_train, scoring="roc_auc", model_name=name)
    cv_scores[name] = (mean_cv, std_cv)

# overfitting provera (train vs test accuracy)
print("\n=== OVERFITTING PROVERA ===")
overfitting_scores = {}
for model, name in zip(models, model_names):
    overfitting_scores[name] = check_overfitting(model, X_train, y_train, X_test, y_test, name)

# spajanje svih metrika u jedan rezultujuci fajl
final_rows = []
for res, name in zip(model_results, model_names):
    of = overfitting_scores[name]
    cv_mean, cv_std = cv_scores[name]
    final_rows.append({
        "Model": res["Model"],
        "Accuracy": res["Accuracy"],
        "Precision": res["Precision"],
        "Recall": res["Recall"],
        "F1": res["F1"],
        "Test_AUC": auc_scores[name],
        "CV_AUC_Mean": cv_mean,
        "CV_AUC_Std": cv_std,
        "Train_Accuracy": of["Train_Accuracy"],
        "Overfitting_Gap": of["Overfitting_Gap"],
    })

results_df = pd.DataFrame(final_rows)
results_df.to_csv(os.path.join(RESULTS_DIR, "final_model_results.csv"), index=False)
print("\n=== FINALNI REZULTATI (sacuvano u results/final_model_results.csv) ===")
print(results_df.to_string(index=False, float_format="%.4f"))

# feature importance - RF (gini) + ostali modeli (permutation importance)
print("\n=== FEATURE IMPORTANCE ===")
plot_feature_importance(rf_model, feature_names, "Random Forest", top_n=len(feature_names))
plt.savefig(os.path.join(RESULTS_DIR, "feature_importance_rf.png"), bbox_inches="tight")
plt.show()

plt_combined = plot_combined_feature_importance(models, model_names, feature_names, X_train, y_train)
plt_combined.savefig(os.path.join(RESULTS_DIR, "feature_importance_combined.png"), bbox_inches="tight")
plt_combined.show()

print("\nGotovo.")
