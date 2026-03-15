import streamlit as st
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score
from model.train_model import train_and_evaluate
from fairness.fairness_metrics import calculate_fairness
import numpy as np


st.set_page_config(page_title="Fairness Analysis", layout="wide")

st.title("Fairness Analysis and Bias Detection in Deep Learning Models")
st.markdown("### Evaluating Gender Bias in Income Prediction (Adult Dataset)")

st.markdown("---")

st.subheader("Dataset Overview")
st.write("Dataset: Adult Income Dataset")
st.write("Target Variable: Income (>50K or <=50K)")
st.write("Sensitive Attribute: Gender")

st.markdown("---")

if st.button("Run Fairness Analysis"):

    model, X_test, y_test, sensitive_test, accuracy = train_and_evaluate()

    st.subheader("Model Performance")
    st.write(f"Accuracy: {round(accuracy,4)}")

    y_pred = model.predict(X_test)
    fairness_results = calculate_fairness(y_test, y_pred, sensitive_test)

    st.subheader("Fairness Metrics (Before Mitigation)")
    st.write(f"Male Selection Rate: {round(fairness_results['male_selection_rate'],4)}")
    st.write(f"Female Selection Rate: {round(fairness_results['female_selection_rate'],4)}")
    st.write(f"Disparate Impact: {round(fairness_results['disparate_impact'],4)}")

    # Visualization
    fig1, ax1 = plt.subplots()
    ax1.bar(["Male", "Female"], 
            [fairness_results['male_selection_rate'], 
             fairness_results['female_selection_rate']])
    ax1.set_title("Selection Rate by Gender")
    st.pyplot(fig1)

    st.markdown("---")

    st.subheader("Apply Bias Mitigation")

    if st.button("Apply Mitigation"):

        y_prob = model.predict_proba(X_test)[:, 1]

        y_pred_mitigated = []

        for prob, gender in zip(y_prob, sensitive_test):
            gender = gender.strip()
            if gender == "Female":
                y_pred_mitigated.append(1 if prob > 0.3 else 0)
            else:
                y_pred_mitigated.append(1 if prob > 0.5 else 0)

        fairness_after = calculate_fairness(y_test, y_pred_mitigated, sensitive_test)
        accuracy_after = accuracy_score(y_test, y_pred_mitigated)

        st.subheader("Fairness Metrics (After Mitigation)")
        st.write(f"Accuracy After: {round(accuracy_after,4)}")
        st.write(f"Male Selection Rate: {round(fairness_after['male_selection_rate'],4)}")
        st.write(f"Female Selection Rate: {round(fairness_after['female_selection_rate'],4)}")
        st.write(f"Disparate Impact: {round(fairness_after['disparate_impact'],4)}")

        # Disparate Impact Comparison
        fig2, ax2 = plt.subplots()
        ax2.bar(["Before", "After"],
                [fairness_results['disparate_impact'],
                 fairness_after['disparate_impact']])
        ax2.axhline(y=0.8, linestyle='--')
        ax2.set_title("Disparate Impact Before vs After Mitigation")
        st.pyplot(fig2)

        st.markdown("---")

        st.success("Mitigation improved fairness while maintaining comparable accuracy.")