import sqlite3

from database import init_db, insert_prediction
from flask import Flask, render_template, request
import numpy as np
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import os
import uuid

app = Flask(__name__)
init_db()

# Debug info
print("Files in current directory:", os.listdir('.'))
print("Files in models folder:", os.listdir('models'))

# === Load Models ===
binary_model_path = "models/lightgbm_ckd_binary_v5.pkl"
multiclass_model_path = "models/lightgbm_ckd_multiclass_v1.pkl"

assert os.path.exists(binary_model_path), f"Binary model not found at {binary_model_path}"
assert os.path.exists(multiclass_model_path), f"Multiclass model not found at {multiclass_model_path}"

model_bin = joblib.load(binary_model_path)
model_multi = joblib.load(multiclass_model_path)

# Accuracy
accuracy_bin = 0.94
accuracy_multi = 0.88

# Features
features = [
    'serum_creatinine', 'gfr', 'bun', 'serum_calcium', 'ana', 'c3_c4',
    'hematuria', 'oxalate_levels', 'urine_ph', 'physical_activity',
    'water_intake', 'smoking', 'alcohol', 'painkiller_usage',
    'family_history', 'weight_changes', 'stress_level', 'months', 'cluster',
    'diet_balanced', 'diet_high_protein', 'diet_low_salt',
    'blood_pressure_transformed'
]

# Stage mapping
stage_mapping = {
    0: 'Stage 1',
    1: 'Stage 2',
    2: 'Stage 3',
    3: 'Stage 4',
    4: 'Stage 5'
}

valid_stages = ["Stage 1", "Stage 2", "Stage 3", "Stage 4", "Stage 5"]

stage_colors = ['#81C784', '#4DB6AC', '#FFF176', '#FFB74D', '#E57373']

# === ROUTES ===

@app.route('/')
def home():
    return render_template("home.html")


@app.route('/predict')
def input_page():
    return render_template("form.html", features=features)

@app.route('/history')
def history():
    conn = sqlite3.connect("predictions.db")
    c = conn.cursor()

    c.execute("SELECT * FROM predictions ORDER BY date DESC")
    data = c.fetchall()

    conn.close()

    return render_template("history.html", data=data)

@app.route('/predict-manual', methods=['POST'])
def predict_manual():
    try:
        input_data = [float(request.form[f]) for f in features]
    except Exception as e:
        return f"Invalid input: {str(e)}"

    X = np.array(input_data).reshape(1, -1)
    pred_ckd = model_bin.predict(X)[0]

    if pred_ckd == 1:
        pred_stage = model_multi.predict(X)[0]
        stage_text = f"Predicted CKD Stage: {stage_mapping.get(pred_stage, 'Unknown')}"
        message = "Unfortunately, signs of CKD have been detected."
        emoji = "😟"
        # 🔥 SAVE TO DATABASE (ADD THIS)
        insert_prediction(
           "Manual",
           "CKD",
            stage_text,
            accuracy_bin
        )
    else:
        stage_text = "No CKD detected."
        message = "Great news! No signs of CKD were found."
        emoji = "😊"

        # SAVE TO DATABASE (ADD THIS)
        insert_prediction(
            "Manual",
            "No CKD",
            "N/A",
            accuracy_bin
        )

    return render_template(
        "manual_prediction_result.html",
        pred_ckd=pred_ckd,
        stage_text=stage_text,
        message=message,
        emoji=emoji,
        accuracy_bin=accuracy_bin,
        accuracy_multi=accuracy_multi
    )

@app.route('/predict-file', methods=['POST'])
def predict_file():
    try:
        file = request.files.get('file')

        if file is None or file.filename == '':
            return "No file uploaded."

        ext = file.filename.split('.')[-1].lower()

        if ext not in ['csv', 'xlsx']:
            return "Only .csv and .xlsx files are supported."

        # Read file
        df = pd.read_csv(file) if ext == 'csv' else pd.read_excel(file)
        df.columns = df.columns.str.strip()

        # Check columns
        if not all(col in df.columns for col in features):
            return f"Missing required columns. Found: {list(df.columns)}"

        # Prediction
        X = df[features]
        pred_ckd = model_bin.predict(X)
        pred_stage = model_multi.predict(X)

        # Add results
        df['CKD Prediction'] = np.where(pred_ckd == 1, "Yes", "No")
        df['CKD Stage'] = [
            stage_mapping.get(stage, "N/A") if pred == 1 else "N/A"
            for stage, pred in zip(pred_stage, pred_ckd)
        ]

        #  SAVE ALL ROWS TO DATABASE
        for i in range(len(df)):
            insert_prediction(
              "File",
               df['CKD Prediction'].iloc[i],
               df['CKD Stage'].iloc[i],
               accuracy_bin
    )
        # === Visualization ===
        stage_counts = df[df['CKD Prediction'] == "Yes"]['CKD Stage'].value_counts()

        # Remove invalid values safely
        valid_stages = ["Stage 1", "Stage 2", "Stage 3", "Stage 4", "Stage 5"]

        labels = []
        sizes = []

        for stage, count in stage_counts.items():
            if stage in valid_stages:
                labels.append(stage)
                sizes.append(count)

        #  Handle no CKD case
        if len(labels) == 0:
            return render_template(
                "batch_file_prediction_result.html",
                df=df.to_html(classes="table table-bordered"),
                pie_chart=None,
                bar_chart=None,
                accuracy_bin=accuracy_bin,
                accuracy_multi=accuracy_multi,
                message="No CKD cases found in file."
            )

        # SAFE color mapping (NO crash possible)
        stage_color_map = {
            "Stage 1": "#81C784",
            "Stage 2": "#4DB6AC",
            "Stage 3": "#FFF176",
            "Stage 4": "#FFB74D",
            "Stage 5": "#E57373"
        }

        colors = [stage_color_map[stage] for stage in labels]

        # Generate charts
        chart_id = uuid.uuid4().hex
        pie_filename = f"pie_{chart_id}.png"
        bar_filename = f"bar_{chart_id}.png"

        pie_path = os.path.join("static", pie_filename)
        bar_path = os.path.join("static", bar_filename)

        # Pie chart
        plt.figure(figsize=(5, 5))
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%')
        plt.title("CKD Stage Distribution")
        plt.savefig(pie_path)
        plt.close()

        # Bar chart
        plt.figure(figsize=(6, 4))
        plt.bar(labels, sizes, color=colors)
        plt.title("CKD Stage Count")
        plt.xlabel("Stage")
        plt.ylabel("Patients")
        plt.savefig(bar_path)
        plt.close()
        return render_template(
            "batch_file_prediction_result.html",
            df=df.to_html(classes="table table-bordered"),
            pie_chart=pie_filename,  
            bar_chart=bar_filename,   
            accuracy_bin=accuracy_bin,
            accuracy_multi=accuracy_multi
        )
    except Exception as e:
        return f"ERROR: {str(e)}"

# === RUN APP ===
if __name__ == '__main__':
    app.run(debug=True)




