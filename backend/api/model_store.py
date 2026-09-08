"""
Drzi aktivni model u memoriji i omogucava zamenu bez restarta servera.

Bez ovoga bi posle svakog pretreniranja morao rucno da restartujes
uvicorn da bi API poceo da koristi novi model.
"""
import os

import joblib

from scripts.training import MODEL_DIR, read_metadata


METADATA_PATH = os.path.join(MODEL_DIR, "metadata.json")


class ModelStore:
    def __init__(self):
        self.model = None
        self.feature_names = None
        self.metadata = None
        self._stamp = None
        self.load()

    def load(self):
        model_path = os.path.join(MODEL_DIR, "model.joblib")
        features_path = os.path.join(MODEL_DIR, "feature_names.joblib")

        if not os.path.exists(model_path):
            raise FileNotFoundError(
                f"Model nije pronadjen ({model_path}). Pokreni prvo: python train_model.py"
            )

        self.model = joblib.load(model_path)
        self.feature_names = joblib.load(features_path)
        self.metadata = read_metadata() or {"version": "rf_v1"}
        self._stamp = self._current_stamp()

    @staticmethod
    def _current_stamp():
        try:
            return os.path.getmtime(METADATA_PATH)
        except OSError:
            return None

    def ensure_fresh(self):
        """Ucitava model ponovo ako je u medjuvremenu pretreniran spolja.

        Bez ovoga bi posle rucnog `python train_model.py` server nastavio
        da koristi stari model sve do restarta.
        """
        if self._current_stamp() != self._stamp:
            self.load()

    @property
    def version(self):
        return self.metadata.get("version", "rf_v1")


store = ModelStore()
