import numpy as np
import pandas as pd

def safe_divide(a, b):
    return a / b if b != 0 else 0

def calculate_fairness(y_true, y_pred, sensitive_attribute):
    sensitive_attribute = pd.Series(sensitive_attribute).astype(str).str.strip()

    df = pd.DataFrame({
        "actual": y_true,
        "predicted": y_pred,
        "group": sensitive_attribute
    })

    male_selection = df[df["group"] == "Male"]["predicted"].mean()
    female_selection = df[df["group"] == "Female"]["predicted"].mean()

    male_selection = 0 if pd.isna(male_selection) else male_selection
    female_selection = 0 if pd.isna(female_selection) else female_selection

    disparate_impact = safe_divide(female_selection, male_selection)
    statistical_parity_difference = female_selection - male_selection

    male_df = df[df["group"] == "Male"]
    female_df = df[df["group"] == "Female"]

    male_accuracy = (male_df["actual"] == male_df["predicted"]).mean() if len(male_df) > 0 else 0
    female_accuracy = (female_df["actual"] == female_df["predicted"]).mean() if len(female_df) > 0 else 0

    male_positive = male_df[male_df["actual"] == 1]
    female_positive = female_df[female_df["actual"] == 1]

    male_tpr = safe_divide((male_positive["predicted"] == 1).sum(), len(male_positive))
    female_tpr = safe_divide((female_positive["predicted"] == 1).sum(), len(female_positive))

    equal_opportunity_difference = female_tpr - male_tpr

    return {
        "male_selection_rate": male_selection,
        "female_selection_rate": female_selection,
        "disparate_impact": disparate_impact,
        "statistical_parity_difference": statistical_parity_difference,
        "male_accuracy": male_accuracy,
        "female_accuracy": female_accuracy,
        "male_tpr": male_tpr,
        "female_tpr": female_tpr,
        "equal_opportunity_difference": equal_opportunity_difference
    }