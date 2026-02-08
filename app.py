from flask import Flask, render_template, request
import numpy as np
import pickle
import sqlite3

app = Flask(__name__)

model = pickle.load(open("model.pkl", "rb"))
le = pickle.load(open("label_encoder.pkl", "rb"))
features = pickle.load(open("features.pkl", "rb"))

@app.route("/", methods=["GET", "POST"])
def home():
    prediction = None
    confidence = None

    if request.method == "POST":
        selected_symptoms = request.form.getlist("symptoms")

        input_data = np.zeros(len(features))
        for symptom in selected_symptoms:
            if symptom in features:
                index = features.index(symptom)
                input_data[index] = 1

        probs = model.predict_proba([input_data])[0]
        pred_index = np.argmax(probs)
        prediction = le.inverse_transform([pred_index])[0]
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

    return render_template("index.html", symptoms=features, prediction=prediction, confidence=confidence)

if __name__ == "__main__":
    app.run(debug=True)

