from typing import Literal

from pydantic import BaseModel

from scripts.mappings import SYMPTOM_MAPPINGS, AGE_MAPPING


class UpitnikInput(BaseModel):
    age: Literal["25-30", "30-35", "35-40", "40-45", "45-50"]
    feeling_sad: Literal["no", "sometimes", "yes"]
    irritable: Literal["no", "sometimes", "yes"]
    trouble_sleeping: Literal["no", "yes", "two or more days a week"]
    concentration_problems: Literal["no", "often", "yes"]
    appetite_problems: Literal["yes", "no", "not at all"]
    guilt: Literal["yes", "no", "maybe"]
    bonding_problems: Literal["yes", "sometimes", "no"]
    suicide_attempt: Literal["no", "yes", "not interested to say"]

    def to_encoded_dict(self) -> dict:
        return {
            "age": AGE_MAPPING[self.age],
            "feeling_sad": SYMPTOM_MAPPINGS["feeling sad or tearful"][self.feeling_sad],
            "irritable": SYMPTOM_MAPPINGS["irritable towards baby & partner"][self.irritable],
            "trouble_sleeping": SYMPTOM_MAPPINGS["trouble sleeping at night"][self.trouble_sleeping],
            "concentration_problems": SYMPTOM_MAPPINGS["problems concentrating or making decision"][self.concentration_problems],
            "appetite_problems": SYMPTOM_MAPPINGS["overeating or loss of appetite"][self.appetite_problems],
            "guilt": SYMPTOM_MAPPINGS["feeling of guilt"][self.guilt],
            "bonding_problems": SYMPTOM_MAPPINGS["problems of bonding with baby"][self.bonding_problems],
            "suicide_attempt": SYMPTOM_MAPPINGS["suicide attempt"][self.suicide_attempt],
        }


class PredictionOutput(BaseModel):
    predicted_risk: int
    predicted_probability: float
    model_version: str
    crisis_flag: bool
    crisis_message: str | None = None


class AnketaInput(UpitnikInput):
    """Same questions as the prediction endpoint, plus a self-assessment answer.

    `feels_depressed` is written to the feeling_depressed column - the target
    variable the model learns to predict. This is a self-assessment question
    (same style as the "Feeling anxious" target column in the Kaggle seed
    dataset), not a clinical diagnosis. (This docstring is exposed in the
    Swagger UI, hence English.)
    """

    feels_depressed: Literal["yes", "no"]

    def to_training_row(self) -> dict:
        row = self.to_encoded_dict()
        row["feeling_depressed"] = 1 if self.feels_depressed == "yes" else 0
        row["source"] = "anketa"
        return row


class ContributionOutput(BaseModel):
    saved: bool
    total_records: int
    survey_records: int
    crisis_flag: bool
    crisis_message: str | None = None
