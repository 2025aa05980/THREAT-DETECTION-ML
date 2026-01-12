
# model/train_models.py

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score, roc_auc_score, precision_score,
    recall_score, f1_score, matthews_corrcoef
)

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier

import xgboost as xgb
import joblib
import os

# Load and preprocess data
def load_and_preprocess(csv_path: str):
    df = pd.read_csv(csv_path)

    # Basic feature engineering Total_Bytes and Bytes_Ratio are created from Bytes_Sent and Bytes_Received features for better model performance
    df['Total_Bytes'] = df['Bytes_Sent'] + df['Bytes_Received']
    df['Bytes_Ratio'] = df['Bytes_Sent'] / (df['Bytes_Received'] + 1)

    # One-hot encode Protocol feature to convert categorical data into numerical format (necessary for ML algorithms that require numerical input)
    df = pd.get_dummies(df, columns=['Protocol'], drop_first=False)

    # Features and target split, remove Label column from features and set it as target variable
    X = df.drop(columns=['Label'])
    y = df['Label']

    # Train-test split with stratification to maintain class distribution in both sets. 
    # 80-20 split is standard for training and evaluation.
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Scale numeric features using StandardScaler for algorithms sensitive to feature scaling
    # z = (x - mean) / stddev
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    return X_train, X_test, X_train_scaled, X_test_scaled, y_train, y_test, scaler, X.columns

def evaluate_model(name, model, X_test, y_test, proba_available=True):
    y_pred = model.predict(X_test)

    metrics = {}
    metrics['accuracy'] = accuracy_score(y_test, y_pred)
    metrics['precision'] = precision_score(y_test, y_pred, zero_division=0)
    metrics['recall'] = recall_score(y_test, y_pred, zero_division=0)
    metrics['f1'] = f1_score(y_test, y_pred, zero_division=0)
    metrics['mcc'] = matthews_corrcoef(y_test, y_pred)

    # Calculate AUC only if probability estimates are available
    # Applicable for models like Logistic Regression, Random Forest, XGBoost, Decision Tree, KNN, etc.
    # proba_available flag indicates if the model supports probability outputs and avoids errors for models that do not
    # predict_proba method returns class probabilities for classification tasks
    if proba_available:
        y_proba = model.predict_proba(X_test)[:, 1]
        metrics['auc'] = roc_auc_score(y_test, y_proba)
    else:
        metrics['auc'] = np.nan

    print(f"\n=== {name} ===")
    for k, v in metrics.items():
        print(f"{k}: {v:.4f}")

    return metrics

def main():
    # Initialize Paths
    base_dir = os.path.dirname(os.path.dirname(__file__))
    data_path = os.path.join(base_dir, 'data', 'ThreatDetection_dataset.csv')
    model_dir = os.path.join(base_dir, 'model')
    os.makedirs(model_dir, exist_ok=True)

    # Load and preprocess data
    (X_train, X_test,
     X_train_scaled, X_test_scaled,
     y_train, y_test, scaler, feature_names) = load_and_preprocess(data_path)

    # Save scaler and feature names for app
    joblib.dump(scaler, os.path.join(model_dir, 'scaler.pkl'))
    joblib.dump(feature_names, os.path.join(model_dir, 'feature_names.pkl'))

    results = {}

    # 1. Logistic Regression
    lr = LogisticRegression(max_iter=1000)
    lr.fit(X_train_scaled, y_train)
    results['Logistic Regression'] = evaluate_model(
        'Logistic Regression', lr, X_test_scaled, y_test
    )
    joblib.dump(lr, os.path.join(model_dir, 'logistic_regression.pkl'))

    # 2. Decision Tree
    dt = DecisionTreeClassifier(random_state=42)
    dt.fit(X_train, y_train)
    results['Decision Tree'] = evaluate_model(
        'Decision Tree', dt, X_test, y_test
    )
    joblib.dump(dt, os.path.join(model_dir, 'decision_tree.pkl'))

    # 3. kNN
    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(X_train_scaled, y_train)
    results['kNN'] = evaluate_model(
        'kNN', knn, X_test_scaled, y_test
    )
    joblib.dump(knn, os.path.join(model_dir, 'knn.pkl'))

    # 4. Naive Bayes (Gaussian)
    nb = GaussianNB()
    nb.fit(X_train, y_train)
    results['Naive Bayes'] = evaluate_model(
        'Naive Bayes', nb, X_test, y_test
    )
    joblib.dump(nb, os.path.join(model_dir, 'naive_bayes.pkl'))

    # 5. Random Forest
    rf = RandomForestClassifier(
        n_estimators=200, random_state=42, n_jobs=-1
    )
    rf.fit(X_train, y_train)
    results['Random Forest'] = evaluate_model(
        'Random Forest', rf, X_test, y_test
    )
    joblib.dump(rf, os.path.join(model_dir, 'random_forest.pkl'))

    # 6. XGBoost
    xgb_clf = xgb.XGBClassifier(
        n_estimators=200,
        learning_rate=0.1,
        max_depth=5,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        eval_metric='logloss'
    )
    xgb_clf.fit(X_train, y_train)
    results['XGBoost'] = evaluate_model(
        'XGBoost', xgb_clf, X_test, y_test
    )
    joblib.dump(xgb_clf, os.path.join(model_dir, 'xgboost.pkl'))

    # Optionally save results to CSV for easy copy into README
    res_df = pd.DataFrame(results).T
    res_df.to_csv(os.path.join(model_dir, 'model_metrics.csv'), index=True)
    print("\nSaved metrics to model/model_metrics.csv")


if __name__ == "__main__":
    main()