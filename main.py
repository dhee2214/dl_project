import pandas as pd
from model.train_model import train_and_evaluate
from fairness.fairness_metrics import calculate_fairness
from fairness.mitigation import apply_threshold_mitigation
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, confusion_matrix


def main():

    # Train model and get results
    results = train_and_evaluate()

    y_test = results["y_test"]
    sensitive_test = results["sensitive_test"]
    y_pred = results["y_pred"]
    y_prob = results["y_prob"]

    print("=== MODEL PERFORMANCE BEFORE MITIGATION ===")
    print("Accuracy:", round(results["accuracy"], 4))
    print("Precision:", round(results["precision"], 4))
    print("Recall:", round(results["recall"], 4))
    print("F1-score:", round(results["f1"], 4))

    print("\nClassification Report (Before Mitigation):")
    print(results["classification_report"])

    print("Confusion Matrix (Before Mitigation):")
    print(results["confusion_matrix"])

    # Fairness before mitigation
    fairness_results = calculate_fairness(y_test, y_pred, sensitive_test)

    print("\n--- FAIRNESS BEFORE MITIGATION ---")
    print("Male Selection Rate:", round(fairness_results["male_selection_rate"], 4))
    print("Female Selection Rate:", round(fairness_results["female_selection_rate"], 4))
    print("Disparate Impact:", round(fairness_results["disparate_impact"], 4))
    print("Statistical Parity Difference:", round(fairness_results["statistical_parity_difference"], 4))
    print("Male Accuracy:", round(fairness_results["male_accuracy"], 4))
    print("Female Accuracy:", round(fairness_results["female_accuracy"], 4))
    print("Male TPR:", round(fairness_results["male_tpr"], 4))
    print("Female TPR:", round(fairness_results["female_tpr"], 4))
    print("Equal Opportunity Difference:", round(fairness_results["equal_opportunity_difference"], 4))

    # Mitigation
    male_threshold = 0.5
    female_threshold = 0.3

    y_pred_mitigated = apply_threshold_mitigation(
        y_prob,
        sensitive_test,
        male_threshold=male_threshold,
        female_threshold=female_threshold
    )

    # Performance after mitigation
    accuracy_after = accuracy_score(y_test, y_pred_mitigated)
    precision_after = precision_score(y_test, y_pred_mitigated)
    recall_after = recall_score(y_test, y_pred_mitigated)
    f1_after = f1_score(y_test, y_pred_mitigated)
    report_after = classification_report(y_test, y_pred_mitigated)
    cm_after = confusion_matrix(y_test, y_pred_mitigated)

    # Fairness after mitigation
    fairness_after = calculate_fairness(y_test, y_pred_mitigated, sensitive_test)

    print("\n=== MODEL PERFORMANCE AFTER MITIGATION ===")
    print("Accuracy:", round(accuracy_after, 4))
    print("Precision:", round(precision_after, 4))
    print("Recall:", round(recall_after, 4))
    print("F1-score:", round(f1_after, 4))

    print("\nClassification Report (After Mitigation):")
    print(report_after)

    print("Confusion Matrix (After Mitigation):")
    print(cm_after)

    print("\n--- FAIRNESS AFTER MITIGATION ---")
    print("Male Selection Rate:", round(fairness_after["male_selection_rate"], 4))
    print("Female Selection Rate:", round(fairness_after["female_selection_rate"], 4))
    print("Disparate Impact:", round(fairness_after["disparate_impact"], 4))
    print("Statistical Parity Difference:", round(fairness_after["statistical_parity_difference"], 4))
    print("Male Accuracy:", round(fairness_after["male_accuracy"], 4))
    print("Female Accuracy:", round(fairness_after["female_accuracy"], 4))
    print("Male TPR:", round(fairness_after["male_tpr"], 4))
    print("Female TPR:", round(fairness_after["female_tpr"], 4))
    print("Equal Opportunity Difference:", round(fairness_after["equal_opportunity_difference"], 4))

    comparison_df = pd.DataFrame({
    "Metric": [
        "Accuracy",
        "Precision",
        "Recall",
        "F1-score",
        "Disparate Impact",
        "Statistical Parity Difference",
        "Equal Opportunity Difference"
    ],
    "Before Mitigation": [
        results["accuracy"],
        results["precision"],
        results["recall"],
        results["f1"],
        fairness_results["disparate_impact"],
        fairness_results["statistical_parity_difference"],
        fairness_results["equal_opportunity_difference"]
    ],
    "After Mitigation": [
        accuracy_after,
        precision_after,
        recall_after,
        f1_after,
        fairness_after["disparate_impact"],
        fairness_after["statistical_parity_difference"],
        fairness_after["equal_opportunity_difference"]
    ]
})

    print("\n=== COMPARISON TABLE ===")
    print(comparison_df.round(4))

    print("\n--- MITIGATION DETAILS ---")
    print("Mitigation Type: Post-processing threshold-based mitigation")
    print("Male Threshold:", male_threshold)
    print("Female Threshold:", female_threshold)

    print("\n--- INTERPRETATION ---")
    if fairness_after["disparate_impact"] >= 0.8:
        print("Fairness after mitigation satisfies the 80% rule.")
    else:
        print("Fairness after mitigation does not satisfy the 80% rule yet.")

    before_gap = abs(1 - fairness_results["disparate_impact"])
    after_gap = abs(1 - fairness_after["disparate_impact"])

    if after_gap < before_gap:
        print("Fairness improved after mitigation.")
    else:
        print("Fairness did not improve significantly after mitigation.")

    if accuracy_after >= results["accuracy"] - 0.02:
        print("Performance remained reasonably stable after mitigation.")
    else:
        print("Performance dropped noticeably after mitigation.")


if __name__ == "__main__":
    main()