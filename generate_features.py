import pandas as pd
import pickle

df = pd.read_csv("training.csv")

symptoms = list(df.columns)
symptoms.remove("prognosis")

pickle.dump(symptoms, open("features.pkl", "wb"))

print("features.pkl generated successfully!")
