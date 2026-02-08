ffrom flask import Flask, render_template, request
import pickle
import numpy as np
import sqlite3

app = Flask(__name__)

model = pickle.load(open("model.pkl", "rb"))
features = pickle.load(open("features.pkl", "rb"))

@app.route("/", methods=["GET", "POST"])
def home():
    prediction = None
    confidence = None

    if request.method == "POST":
        selected_symptoms = request.form.getlist("symptoms")
        input_data = [1 if symptom in selected_symptoms else 0 for symptom in features]

        probs = model.predict_proba([input_data])[0]
        pred_index = np.argmax(probs)
        prediction = model.classes_[pred_index]   # <-- THIS LINE FIXES IT
        confidence = round(probs[pred_index] * 100, 2)

        conn = sqlite3.connect("symptom_disease.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (symptoms, predicted_disease, confidence) VALUES (?, ?, ?)",
            (", ".join(selected_symptoms), prediction, confidence),
        )
        conn.commit()
        conn.close()

    return render_template("index.html", features=features, prediction=prediction, confidence=confidence)

if __name__ == "__main__":
    print("Loaded features:", features)

    app.run(debug=True)
