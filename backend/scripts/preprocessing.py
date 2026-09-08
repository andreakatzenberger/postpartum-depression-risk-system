import os

import pandas as pd
from sklearn.model_selection import train_test_split

from scripts.mappings import SYMPTOM_MAPPINGS, AGE_MAPPING


def _is_text_column(series):
    # pandas 3 tipizira string kolone kao 'str', starije verzije kao 'object'
    return pd.api.types.is_string_dtype(series) or series.dtype == object


def preprocess_data():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_file = os.path.join(base_dir, "data", "data.csv")
    df = pd.read_csv(input_file)

    # ceo fajl u lowercase
    df.columns = [col.strip().lower() for col in df.columns]

    for col in df.columns:
        if _is_text_column(df[col]):
            df[col] = df[col].astype(str).str.strip().str.lower()

    print("fajl u lowercase")

    #uklanjamo timestamp jer je irelevantan
    if "timestamp" in df.columns:
        df = df.drop(columns=["timestamp"])

    print("ukloni timestamp")

    #primenjujemo mapiranja gde mapiranja postoje
    for col, mapping in SYMPTOM_MAPPINGS.items():
        if col in df.columns:
            df[col] = df[col].map(mapping)

    #popunjavamo median vrednostima nedostajuce vrednosti u kolonama
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            df[col] = df[col].fillna(df[col].median(skipna=True))
    print("popuni medijan vrednostima")

    #mapiramo godine na kraju
    for col in df.columns:
        if _is_text_column(df[col]):
            if df[col].astype(str).str.match(r"^\d{2}-\d{2}$").any():
                df[col] = df[col].map(AGE_MAPPING)

                print("mapirao godine")

    #cuvanje fajla
    data_dir = os.path.join(base_dir, "data")
    df.to_csv(os.path.join(data_dir, "data_preprocessed.csv"), index=False)
    print("preprocesiranje zavrseno")

    train_df, test_df = train_test_split(df, test_size=0.2, random_state=42, shuffle=True)


    train_df.to_csv(os.path.join(data_dir, "data_train.csv"), index=False)
    test_df.to_csv(os.path.join(data_dir, "data_test.csv"), index=False)

    print("trening i evaluacioni podaci podeljeni 80:20")

    return train_df, test_df

