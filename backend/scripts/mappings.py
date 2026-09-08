"""
Jedinstveni izvor istine za mapiranje odgovora iz upitnika u brojeve
koje model ocekuje. Koristi ih i preprocessing.py (trening) i API
(predikcija), da nikad ne dodju iz sinhrona.
"""

SYMPTOM_MAPPINGS = {
    "trouble sleeping at night": {"no": 0, "yes": 1, "two or more days a week": 0.5},
    "problems concentrating or making decision": {"no": 0, "often": 0.5, "yes": 1},
    "overeating or loss of appetite": {"yes": 1, "no": 0, "not at all": 0},
    "feeling of guilt": {"yes": 1, "no": 0, "maybe": 0.5},
    "problems of bonding with baby": {"yes": 1, "sometimes": 0.5, "no": 0},
    "suicide attempt": {"no": 0, "yes": 1, "not interested to say": 0.9},
    "irritable towards baby & partner": {"no": 0, "sometimes": 0.5, "yes": 1},
    "feeling sad or tearful": {"no": 0, "sometimes": 0.5, "yes": 1},
    "feeling anxious": {"no": 0, "yes": 1},
}

AGE_MAPPING = {
    "25-30": 1,
    "30-35": 2,
    "35-40": 3,
    "40-45": 4,
    "45-50": 5,
}

# skraceni (snake_case) naziv atributa -> tacan naziv kolone kako se zove
# u trening skupu (i time u feature_names.joblib). API prima skraceno ime,
# ali model mora dobiti podatke pod ORIGINALNIM imenom i u ISTOM redosledu
# kojim je treniran - zato ovo mapiranje postoji.
FEATURE_NAME_MAP = {
    "age": "age",
    "feeling_sad": "feeling sad or tearful",
    "irritable": "irritable towards baby & partner",
    "trouble_sleeping": "trouble sleeping at night",
    "concentration_problems": "problems concentrating or making decision",
    "appetite_problems": "overeating or loss of appetite",
    "guilt": "feeling of guilt",
    "bonding_problems": "problems of bonding with baby",
    "suicide_attempt": "suicide attempt",
}
