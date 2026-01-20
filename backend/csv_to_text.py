import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "..", "data", "Crop_recommendation.csv")
TXT_PATH = os.path.join(BASE_DIR, "..", "data", "agriculture.txt")

print(f"Reading CSV from: {CSV_PATH}")

df = pd.read_csv(CSV_PATH)

lines = []

for _, row in df.iterrows():
    line = (
        f"For soil with Nitrogen {row['N']}, Phosphorus {row['P']}, "
        f"Potassium {row['K']}, temperature {row['temperature']} degree Celsius, "
        f"humidity {row['humidity']} percent, pH {row['ph']}, "
        f"and rainfall {row['rainfall']} mm, "
        f"the recommended crop is {row['label']}."
    )
    lines.append(line)

# Ensure data folder exists
os.makedirs(os.path.dirname(TXT_PATH), exist_ok=True)

with open(TXT_PATH, "w", encoding="latin-1") as f:
    f.write("\n".join(lines))

print("✅ CSV converted to text successfully")
print(f"📄 Text file created at: {TXT_PATH}")
