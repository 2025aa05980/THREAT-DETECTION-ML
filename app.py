# app.py

import streamlit as st
import requests
import pandas as pd
import numpy as np
import joblib
import os

from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score, matthews_corrcoef,
    confusion_matrix, classification_report
)
import matplotlib.pyplot as plt
import seaborn as sns


@st.cache_resource
def load_artifacts():
    base_dir = os.path.dirname(__file__)
    model_dir = os.path.join(base_dir, 'model')

    scaler = joblib.load(os.path.join(model_dir, 'scaler.pkl'))
    feature_names = joblib.load(os.path.join(model_dir, 'feature_names.pkl'))

    models = {
        "Logistic Regression": joblib.load(os.path.join(model_dir, 'logistic_regression.pkl')),
        "Decision Tree": joblib.load(os.path.join(model_dir, 'decision_tree.pkl')),
        "kNN": joblib.load(os.path.join(model_dir, 'knn.pkl')),
        "Naive Bayes": joblib.load(os.path.join(model_dir, 'naive_bayes.pkl')),
        "Random Forest": joblib.load(os.path.join(model_dir, 'random_forest.pkl')),
        "XGBoost": joblib.load(os.path.join(model_dir, 'xgboost.pkl'))
    }

    return scaler, feature_names, models


def preprocess_input(df: pd.DataFrame, feature_names):
    # assume same preprocessing as in train_models.py

    if 'Total_Bytes' not in df.columns:
        df['Total_Bytes'] = df['Bytes_Sent'] + df['Bytes_Received']
    if 'Bytes_Ratio' not in df.columns:
        df['Bytes_Ratio'] = df['Bytes_Sent'] / (df['Bytes_Received'] + 1)

    df = pd.get_dummies(df, columns=['Protocol'], drop_first=False)

    # Ensure all training-time feature columns exist
    for col in feature_names:
        if col not in df.columns:
            df[col] = 0

    df = df[feature_names]
    return df


def main():
    st.title("Network Threat Detection - ML Model Comparison")

    st.markdown("""
    <div style="padding:12px; border:1px solid #ccc; border-radius:8px;">
        <h4>Machine Learning – Assignment 2 – Section 4</h4>
        <p><strong>Name:</strong> Thanigaivel S<br>
        <strong>BITS ID:</strong> 2025AA05980</p>
    </div>
    """, unsafe_allow_html=True)

    st.write(
        "Upload a CSV file with network flow data and choose a model to predict "
        "whether the traffic is benign or malicious."
    )

    scaler, feature_names, models = load_artifacts()

    model_name = st.selectbox(
        "Select a model",
        list(models.keys())
    )
    model = models[model_name]

    st.subheader("Download Sample Dataset")

    dataset_url = "https://raw.githubusercontent.com/2025aa05980/THREAT-DETECTION-ML/main/data/ThreatDetection_dataset.csv"

    # Fetch the file content
    response = requests.get(dataset_url)
    csv_data = response.content

    st.download_button(
        label="📥 Download ThreatDetection_dataset.csv",
        data=csv_data,
        file_name="ThreatDetection_dataset.csv",
        mime="text/csv"
    )

    uploaded_file = st.file_uploader(
        "Upload test CSV file",
        type=["csv"],
        help="Use the same feature schema as the training data"
    )

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        st.subheader("Preview of uploaded data")
        st.dataframe(df.head())

        has_label = 'Label' in df.columns

        if has_label:
            y_true = df['Label']
            X = df.drop(columns=['Label'])
        else:
            y_true = None
            X = df

        X_proc = preprocess_input(X, feature_names)

        # Decide whether to scale
        if model_name in ["Logistic Regression", "kNN"]:
            X_model = scaler.transform(X_proc)
        else:
            X_model = X_proc

        y_pred = model.predict(X_model)

        st.subheader("Predictions")
        st.write(pd.DataFrame({
            "Predicted_Label": y_pred
        }).head(20))

        if has_label:
            st.subheader("Evaluation Metrics (on uploaded data)")

            acc = accuracy_score(y_true, y_pred)
            prec = precision_score(y_true, y_pred, zero_division=0)
            rec = recall_score(y_true, y_pred, zero_division=0)
            f1 = f1_score(y_true, y_pred, zero_division=0)
            mcc = matthews_corrcoef(y_true, y_pred)

            # AUC, if probability available
            if hasattr(model, "predict_proba"):
                y_proba = model.predict_proba(X_model)[:, 1]
                auc = roc_auc_score(y_true, y_proba)
            else:
                auc = np.nan

            st.write(f"**Accuracy:** {acc:.4f}")
            st.write(f"**Precision:** {prec:.4f}")
            st.write(f"**Recall:** {rec:.4f}")
            st.write(f"**F1 Score:** {f1:.4f}")
            st.write(f"**MCC:** {mcc:.4f}")
            st.write(f"**AUC:** {auc:.4f}" if not np.isnan(auc) else "**AUC:** N/A")

            # Confusion matrix
            cm = confusion_matrix(y_true, y_pred)
            fig, ax = plt.subplots()
            sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax)
            ax.set_xlabel("Predicted")
            ax.set_ylabel("Actual")
            ax.set_title("Confusion Matrix")
            st.pyplot(fig)

            st.subheader("Classification Report")
            st.text(classification_report(y_true, y_pred))

    else:
        st.info("Please upload a CSV file to begin.")


if __name__ == "__main__":
    main()