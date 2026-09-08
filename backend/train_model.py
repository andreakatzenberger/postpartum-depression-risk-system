"""
Trenira model na podacima IZ BAZE (Kaggle seed + anketni doprinosi)
i snima ga za koriscenje u API-ju.

Isto ovo radi i dugme "Pretreniraj" na admin stranici - razlika je
sto ova skripta uvek snima novi model, dok admin endpoint snima samo
ako je novi bolji od trenutnog (champion/challenger).

Pokretanje:
    python train_model.py
"""
from api.database import engine
from scripts.training import train_challenger, save_model, next_version, evaluate_champion


def main():
    champion_metrics = evaluate_champion(engine)
    model, feature_names, metrics, stats = train_challenger(engine)

    print(f"Podaci: {stats['rows_total']} redova "
          f"(kaggle={stats['rows_kaggle']}, anketa={stats['rows_anketa']})")
    print(f"Trening: {stats['rows_train']} | Holdout: {stats['rows_holdout']}")

    if champion_metrics:
        print(f"\nTrenutni model : AUC={champion_metrics['auc']} "
              f"acc={champion_metrics['accuracy']} f1={champion_metrics['f1']}")
    print(f"Novi model     : AUC={metrics['auc']} "
          f"acc={metrics['accuracy']} f1={metrics['f1']}")

    version = next_version()
    metadata = save_model(model, feature_names, metrics, stats, version)
    print(f"\nSacuvano kao {metadata['version']} ({metadata['trained_at']})")


if __name__ == "__main__":
    main()
