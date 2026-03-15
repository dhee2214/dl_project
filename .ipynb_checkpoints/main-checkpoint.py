from model.train_model import train_and_evaluate
from fairness.fairness_metrics import calculate_fairness
from sklearn.metrics import accuracy_score


def main():

    # Train model and get results
    model, X_test, y_test, sensitive_test, accuracy = train_and_evaluate()

    print("Model Accuracy:", round(accuracy, 4))

    # Original predictions
    y_pred = model.predict(X_test)

    fairness_results = calculate_fairness(y_test, y_pred, sensitive_test)

    print("\n--- Fairness Before Mitigation ---")
    print("Male Selection Rate:", round(fairness_results["male_selection_rate"], 4))
    print("Female Selection Rate:", round(fairness_results["female_selection_rate"], 4))
    print("Disparate Impact:", round(fairness_results["disparate_impact"], 4))

    # Threshold mitigation
    y_prob = model.predict_proba(X_test)[:, 1]

    y_pred_mitigated = []

    for prob, gender in zip(y_prob, sensitive_test):
        gender = gender.strip()
        if gender == "Female":
            y_pred_mitigated.append(1 if prob > 0.3 else 0)
        else:
            y_pred_mitigated.append(1 if prob > 0.5 else 0)

    # Fairness after mitigation
    fairness_after = calculate_fairness(y_test, y_pred_mitigated, sensitive_test)

    accuracy_after = accuracy_score(y_test, y_pred_mitigated)

    print("\n--- Fairness After Mitigation ---")
    print("Accuracy After:", round(accuracy_after, 4))
    print("Male Selection Rate:", round(fairness_after["male_selection_rate"], 4))
    print("Female Selection Rate:", round(fairness_after["female_selection_rate"], 4))
    print("Disparate Impact:", round(fairness_after["disparate_impact"], 4))


if __name__ == "__main__":
    main()