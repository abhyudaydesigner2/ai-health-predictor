import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Load dataset
data = pd.read_csv("Training.csv")

# Remove unnamed columns if any
data = data.loc[:, ~data.columns.str.contains('^Unnamed')]

# Separate features and label
X = data.drop("prognosis", axis=1)
y = data["prognosis"]

# Encode labels
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# Train model
model = RandomForestClassifier(n_estimators=300, random_state=42)
model.fit(X, y_encoded)

# Save everything
pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(le, open("label_encoder.pkl", "wb"))
pickle.dump(list(X.columns), open("features.pkl", "wb"))

print("Model trained and saved successfully!")

