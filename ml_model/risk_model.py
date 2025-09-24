# ml_model/risk_model.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

# Load dataset
data = pd.read_csv("data/realistic_device_data_small.csv")

# Features and target
X = data[['firewall', 'vulnerabilities', 'bandwidth', 'latency']]
y = data['secure']

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train RandomForest model
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Evaluate model
y_pred = clf.predict(X_test)
print(" Accuracy:", accuracy_score(y_test, y_pred))
print("\n Classification Report:\n", classification_report(y_test, y_pred))

# Function to predict new devices
def predict_security(devices_df):
    """
    devices_df: DataFrame with columns ['firewall','vulnerabilities','bandwidth','latency']
    returns: list of 0/1 secure labels
    """
    return clf.predict(devices_df)
