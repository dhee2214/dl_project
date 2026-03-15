import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score


def train_and_evaluate():

    # Load dataset
    columns = [
        "age", "workclass", "fnlwgt", "education", "education-num",
        "marital-status", "occupation", "relationship", "race",
        "gender", "capital-gain", "capital-loss", "hours-per-week",
        "native-country", "income"
    ]

    data = pd.read_csv("data/adult.data", names=columns)

    # Replace missing values
    data.replace(" ?", np.nan, inplace=True)
    data.dropna(inplace=True)

    # Convert income to binary
    data["income"] = data["income"].apply(lambda x: 1 if ">50K" in x else 0)

    # Separate features and target
    X = data.drop("income", axis=1)
    y = data["income"]

    # Store sensitive attribute
    sensitive = X["gender"]
    X = X.drop("gender", axis=1)

    # One-hot encoding
    X = pd.get_dummies(X, drop_first=True)

    # Train-test split
    X_train, X_test, y_train, y_test, sensitive_train, sensitive_test = train_test_split(
        X, y, sensitive, test_size=0.2, random_state=42
    )

    # Scale features
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Train model
    model = MLPClassifier(hidden_layer_sizes=(64, 32),
                          activation='relu',
                          max_iter=200,
                          random_state=42)

    model.fit(X_train, y_train)

    # Predictions
    y_pred = model.predict(X_test)

    # Accuracy
    accuracy = accuracy_score(y_test, y_pred)

    return model, X_test, y_test, sensitive_test, accuracy