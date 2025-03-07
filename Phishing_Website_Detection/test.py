import numpy as np
import pandas as pd
import joblib
import tensorflow as tf
import matplotlib.pyplot as plt
import seaborn as sns
from tensorflow.keras.models import load_model
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
     confusion_matrix, roc_curve, auc
)
from sklearn.preprocessing import StandardScaler

# Load trained models
rf_model = joblib.load("new_app/models/random_forest_model.pkl")
scaler = joblib.load("new_app/models/scaler.pkl")
gru_model = load_model("new_app/models/gru_model.h5")

# Load test dataset
file_path = "test_feature_dataset.csv"  # Path to test dataset
df = pd.read_csv(file_path)

# Separate features and target variable
X_test = df.drop(columns=['label'])
y_test = df['label']  # 1 = Phishing, 0 = Legitimate

# Scale features
X_test_scaled = scaler.transform(X_test)

# Reshape for GRU model (3D input)
X_test_seq = X_test_scaled.reshape((X_test_scaled.shape[0], X_test_scaled.shape[1], 1))

# 1️⃣ **Evaluate Random Forest**
rf_preds = rf_model.predict(X_test_scaled)
rf_probs = rf_model.predict_proba(X_test_scaled)[:, 1]  # Probability scores

# 2️⃣ **Evaluate GRU Model**
gru_probs = gru_model.predict(X_test_seq).flatten()
gru_preds = (gru_probs > 0.5).astype(int)

# 3️⃣ **Evaluate Hybrid Model**
hybrid_probs = (0.6 * rf_probs + 0.4 * gru_probs)
hybrid_preds = (hybrid_probs > 0.5).astype(int)

# Compute evaluation metrics
def evaluate_model(name, y_true, y_pred):
    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred)
    rec = recall_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)
    return [name, acc, prec, rec, f1]

# Store results
results = []
results.append(evaluate_model("Random Forest", y_test, rf_preds))
results.append(evaluate_model("GRU", y_test, gru_preds))
results.append(evaluate_model("Hybrid Model", y_test, hybrid_preds))

# Convert results into DataFrame
results_df = pd.DataFrame(results, columns=["Model", "Accuracy", "Precision", "Recall", "F1-Score"])
print("\n📊 **Model Performance Metrics**")
print(results_df)

# Save results to CSV
results_df.to_csv("model_performance_metrics.csv", index=False)

# Plot Confusion Matrices
def plot_confusion_matrix(y_true, y_pred, title):
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(5, 4))
    sns.heatmap(cm, annot=True, fmt='d', cmap="Blues", xticklabels=["Legitimate", "Phishing"], yticklabels=["Legitimate", "Phishing"])
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.title(title)
    plt.show()

# Generate confusion matrices
plot_confusion_matrix(y_test, rf_preds, "Random Forest Confusion Matrix")
plot_confusion_matrix(y_test, gru_preds, "GRU Confusion Matrix")
plot_confusion_matrix(y_test, hybrid_preds, "Hybrid Model Confusion Matrix")

# Generate ROC Curves
def plot_roc_curve(y_true, y_probs, model_name):
    fpr, tpr, _ = roc_curve(y_true, y_probs)
    roc_auc = auc(fpr, tpr)
    plt.plot(fpr, tpr, label=f"{model_name} (AUC = {roc_auc:.2f})")

plt.figure(figsize=(8, 6))
plot_roc_curve(y_test, rf_probs, "Random Forest")
plot_roc_curve(y_test, gru_probs, "GRU")
plot_roc_curve(y_test, hybrid_probs, "Hybrid Model")
plt.plot([0, 1], [0, 1], "k--")  # Diagonal line
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curves for Phishing Detection")
plt.legend()
plt.show()

print("\n✅ Model testing completed! Results saved in 'model_performance_metrics.csv'")
