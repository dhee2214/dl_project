import numpy as np

def apply_threshold_mitigation(y_prob, sensitive_attribute, male_threshold=0.5, female_threshold=0.3):
    adjusted_predictions = []

    for prob, group in zip(y_prob, sensitive_attribute):
        if str(group).strip() == "Female":
            threshold = female_threshold
        else:
            threshold = male_threshold

        adjusted_predictions.append(1 if prob >= threshold else 0)

    return np.array(adjusted_predictions)