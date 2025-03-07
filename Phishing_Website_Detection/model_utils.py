import joblib
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import load_model
from feature_extraction import extract_features

# Load models once to save time
rf_model = joblib.load('models/random_forest_model.pkl')
scaler = joblib.load('models/scaler.pkl')
gru_model = load_model('models/gru_model.h5')

def predict_hybrid(url):
    """Extract features, scale them, and use RF + GRU for prediction."""
    features_df = extract_features(url)
    features_scaled = scaler.transform(features_df)

    # RF Prediction
    rf_pred = rf_model.predict(features_scaled)

    # GRU Prediction
    features_seq = features_scaled.reshape((features_scaled.shape[0], features_scaled.shape[1], 1))
    gru_pred = (gru_model.predict(features_seq) > 0.5).astype(int).flatten()

    # Hybrid Prediction (Weighted)
    hybrid_pred = (0.6 * rf_pred + 0.4 * gru_pred).round().astype(int)
    
    return "Phishing" if hybrid_pred[0] == 1 else "Legitimate"
