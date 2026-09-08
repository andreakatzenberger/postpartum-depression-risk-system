from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB, ComplementNB, CategoricalNB
from scripts.utils import evaluate_model

def train_naive_bayes(
    X_train,
    X_test,
    y_train,
    y_test,
    model_type: str = "gaussian",
    var_smoothing: float = 1e-09,
    alpha: float = 1.0,
    fit_prior: bool = True,
    class_prior=None,
    binarize=None,
    norm=False,
    min_categories=None,
):
    """
    train a naive bayes variant selectable via model_type.

    model_type:
      - 'gaussian' (default): uses GaussianNB(var_smoothing)
      - 'multinomial': MultinomialNB(alpha, fit_prior, class_prior)
      - 'complement': ComplementNB(alpha, fit_prior, class_prior, norm)
      - 'bernoulli': BernoulliNB(alpha, binarize, fit_prior, class_prior)
      - 'categorical': CategoricalNB(alpha, fit_prior, class_prior, min_categories, var_smoothing)
    """

    model_name = "Naive Bayes"

    if model_type == "gaussian":
        model = GaussianNB(var_smoothing=var_smoothing)
        model_name += f" Gaussian (var_smoothing={var_smoothing})"
    elif model_type == "multinomial":
        model = MultinomialNB(alpha=alpha, fit_prior=fit_prior, class_prior=class_prior)
        model_name += f" Multinomial (alpha={alpha})"
    elif model_type == "complement":
        model = ComplementNB(alpha=alpha, fit_prior=fit_prior, class_prior=class_prior, norm=norm)
        model_name += f" Complement (alpha={alpha}, norm={norm})"
    elif model_type == "bernoulli":
        model = BernoulliNB(alpha=alpha, binarize=binarize, fit_prior=fit_prior, class_prior=class_prior)
        model_name += f" Bernoulli (alpha={alpha}, binarize={binarize})"
    elif model_type == "categorical":
        model = CategoricalNB(alpha=alpha, fit_prior=fit_prior, class_prior=class_prior, min_categories=min_categories)
        model_name += f" Categorical (alpha={alpha})"
    else:
        # fallback to gaussian to keep backward-compatible behaviour
        model = GaussianNB(var_smoothing=var_smoothing)
        model_name += f" Gaussian (var_smoothing={var_smoothing})"

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    results = evaluate_model(model_name, y_test, y_pred)
    return results, model