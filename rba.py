import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Define the mapping for device types
device_type_mapping = {
    "desktop": 1,
    "tablet": 2,
    "mobile": 3,
    "bot": 4,
    "unknown": 5
}

# Load data
df = pd.read_csv('processed_fingerprints.csv')

# Split the data into test and training sets
x = df[['IP Address', 'Browser Name and Version', 'OS Name and Version', 'Device Type', 'Is Attack IP', 'Is Account Takeover']] 
y = df['Login Successful'] 
# 80-20 split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=1111)

# Initialize the Random Forest Classifier
rf_model = RandomForestClassifier(n_estimators=100, random_state=1111)

# Train the model
rf_model.fit(x_train, y_train)

# Make predictions
y_pred = rf_model.predict(x_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)
print("Classification Report:\n", classification_report(y_test, y_pred))

# Feature importance
importances = rf_model.feature_importances_
feature_names = x.columns
print("Feature Importances:")
for name, importance in zip(feature_names, importances):
    print(f"{name}: {importance:.4f}")

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
tn, fp, fn, tp = cm.ravel()

# Create a DataFrame to display the results
results_df = pd.DataFrame({
    'Metric': ['True Positives (TP)', 'False Positives (FP)', 'True Negatives (TN)', 'False Negatives (FN)'],
    'Count': [tp, fp, tn, fn],
    'Description': [
        'Correctly predicted successful logins',
        'Predicted failure but should have been success',
        'Correctly predicted failed logins',
        'Predicted success but should have been failure'
    ]
})

# Display the results as a table
print("\nModel Evaluation Results:")
print(results_df)

# Find False Positives: Predicted 1 (success) but actual 0 (failure)
false_positives = x_test[(y_pred == 1) & (y_test == 0)]

# Display False Positives
print("\nFalse Positives (Predicted Success, Actual Failure):")
print(len(false_positives))
