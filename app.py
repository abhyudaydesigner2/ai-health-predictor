from flask import Flask, render_template, request
import numpy as np
import pickle
import sqlite3
import os

app = Flask(__name__)

# Load model and symptoms
model = pickle.load(open("model.pkl", "rb"))
symptoms = pickle.load(open("symptoms.pkl", "rb"))

# Load disease labels (create once if not exists)
if not os.path.exists("disease_labels.pkl"):
    disease_labels = [
        "Fungal infection", "Allergy", "GERD", "Chronic cholestasis", "Drug Reaction",
        "Peptic ulcer disease", "AIDS", "Diabetes", "Gastroenteritis", "Bronchial Asthma",
        "Hypertension", "Migraine", "Cervical spondylosis", "Paralysis (brain hemorrhage)",
        "Jaundice", "Malaria", "Chicken pox", "Dengue", "Typhoid", "hepatitis A",
        "Hepatitis B", "Hepatitis C", "Hepatitis D", "Hepatitis E", "Alcoholic hepatitis",
        "Tuberculosis", "Common Cold", "Pneumonia", "Dimorphic hemorrhoids (piles)",
        "Heart attack", "Varicose veins", "Hypothyroidism", "Hyperthyroidism",
        "Hypoglycemia", "Osteoarthritis", "Arthritis", "Vertigo (Paroxysmal Positional Vertigo)",
        "Acne", "Urinary tract infection", "Psoriasis", "Impetigo"
    ]
    with open("disease_labels.pkl", "wb") as f:
        pickle.dump(disease_labels, f)
else:
    disease_labels = pickle.load(open("disease_labels.pkl", "rb"))


# Database setup
def init_db():
    conn = sqlite3.connect("symptom_disease.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symptoms TEXT,
            predicted_disease TEXT,
            confidence REAL
        )
    """)
    conn.commit()
    conn.close()

init_db()


@app.route("/", methods=["GET", "POST"])
def home():
    prediction = None
    confidence = None

    if request.method == "POST":
        selected_symptoms = request.form.getlist("symptoms")

        input_data = [1 if symptom in selected_symptoms else 0 for symptom in symptoms]
        input_data = np.array(input_data).reshape(1, -1)

        probs = model.predict_proba(input_data)[0]
        pred_index = np.argmax(probs)
        prediction = disease_labels[pred_index]
        confidence = round(probs[pred_index] * 100, 2)

        # Save to database
        conn = sqlite3.connect("symptom_disease.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (symptoms, predicted_disease, confidence) VALUES (?, ?, ?)",
            (", ".join(selected_symptoms), prediction, confidence),
        )
        conn.commit()
        conn.close()

    return render_template("index.html", symptoms=symptoms, prediction=prediction, confidence=confidence)


if __name__ == "__main__":
    app.run(debug=True)