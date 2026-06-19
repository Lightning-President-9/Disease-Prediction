from flask import Flask, render_template, request, jsonify
from pathlib import Path
import numpy as np
import joblib
import json
from dotenv import load_dotenv
import os
import plotly
import pandas as pd
from plotly.utils import PlotlyJSONEncoder
import plotly.express as px
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import warnings
warnings.filterwarnings("ignore")

load_dotenv()


def safe_value(v):
    if pd.isna(v):
        return "Not Available"
    return v


app = Flask(__name__)

limiter = Limiter(
    get_remote_address,
    storage_uri=os.environ["REDIS_URL"],
    app=app,
    default_limits=["100/day"],
)

# PATHS
BASE = Path(__file__).resolve().parent
P = BASE / "Pickle Files"

MODEL = joblib.load(P / "disease_rf_model.pkl")
ENCODER = joblib.load(P / "label_encoder.pkl")
TRAIN_DF = joblib.load(P / "training_dataset.pkl")
HEALTH_DF = joblib.load(P / "healthcare_dataset.pkl")

SYMPTOMS = TRAIN_DF.drop("prognosis", axis=1).columns.tolist()

# ROUTES
@app.route("/")
def index():
    return render_template("index.html", symptoms=SYMPTOMS)


@app.route("/predict", methods=["GET"])
@limiter.limit("10/minute")
def predict():
    DISEASE_NAME_MAPPING = {
        "(vertigo) Paroymsal  Positional Vertigo": "Benign paroxysmal positional vertigo (BPPV)",
        "acne": "Acne",
        "aids": "HIV/AIDS",
        "alcoholic hepatitis": "Alcoholic hepatitis",
        "allergy": {
            "primary": "Dust mite allergy",
            "related": [
                "Dust mite allergy",
                "Egg allergy",
                "Food allergy",
                "Latex allergy",
                "Milk allergy",
                "Mold allergy",
                "Nickel allergy",
                "Peanut allergy",
                "Penicillin allergy",
                "Pet allergy",
                "Shellfish allergy",
                "Wheat allergy",
            ],
        },
        "arthritis": {
            "primary": "Rheumatoid arthritis",
            "related": [
                "Thumb arthritis",
                "Osteoarthritis",
                "Septic arthritis",
                "Juvenile idiopathic arthritis",
                "Psoriatic arthritis",
                "Reactive arthritis",
                "Rheumatoid arthritis",
            ],
        },
        "bronchial asthma": {
            "primary": "Childhood asthma",
            "related": [
                "Childhood asthma",
                "Exercise-induced asthma",
                "Occupational asthma",
            ],
        },
        "cervical spondylosis": "Cervical spondylosis",
        "chicken pox": "Chickenpox",
        "chronic cholestasis": {
            "primary": "Primary biliary cholangitis",
            "related": [
                "Chronic lymphocytic leukemia",
                "Chronic myelogenous leukemia",
                "Chronic exertional compartment syndrome",
                "Myalgic encephalomyelitis/chronic fatigue syndrome (ME/CFS)",
                "Chronic kidney disease",
                "Chronic sinusitis",
                "Chronic cough",
                "Chronic daily headaches",
                "Chronic hives",
                "Chronic pelvic pain",
            ],
        },
        "common cold": "Common cold",
        "dengue": "Dengue fever",
        "diabetes": {
            "primary": "Diabetes",
            "related": [
                "Diabetes",
                "Gestational diabetes",
                "Type 1 diabetes",
                "Type 1 diabetes in children",
                "Type 2 diabetes",
                "Type 2 diabetes in children",
                "Prediabetes",
            ],
        },
        "dimorphic hemmorhoids(piles)": "Hemorrhoids",
        "drug reaction": "Drug addiction (substance use disorder)",
        "fungal infection": {
            "primary": "Athlete's foot",
            "related": [
                "Athlete's foot",
                "Ringworm (body)",
                "Ringworm (scalp)",
                "Jock itch",
                "Nail fungus",
                "Tinea versicolor",
                "Valley fever",
                "Yeast infection (vaginal)",
            ],
        },
        "gastroenteritis": "Viral gastroenteritis (stomach flu)",
        "gerd": "Gastroesophageal reflux disease (GERD)",
        "heart attack": "Heart attack",
        "hepatitis a": "Hepatitis A",
        "hepatitis b": "Hepatitis B",
        "hepatitis c": "Hepatitis C",
        "hepatitis d": "Hepatitis D",
        "hepatitis e": "Hepatitis E",
        "hypertension": {
            "primary": "High blood pressure (hypertension)",
            "related": [
                "High blood pressure (hypertension)",
                "Pulmonary hypertension",
                "Pseudotumor cerebri (idiopathic intracranial hypertension)",
                "Secondary hypertension",
            ],
        },
        "hyperthyroidism": "Hyperthyroidism (overactive thyroid)",
        "hypoglycemia": {
            "primary": "Hypoglycemia",
            "related": ["Hypoglycemia", "Diabetic hypoglycemia"],
        },
        "hypothyroidism": "Hypothyroidism (underactive thyroid)",
        "migraine": "Migraine",
        "osteoarthristis": "Osteoarthritis",
        "peptic ulcer diseae": "Peptic ulcer",
        "tuberculosis": "Tuberculosis",
        "urinary tract infection": "Urinary tract infection (UTI)",
    }

    symptoms = request.args.getlist("symptoms")
    if not symptoms:
        return jsonify({"error": "No symptoms"}), 400

    x = np.zeros((1, len(SYMPTOMS)))
    for s in symptoms:
        if s in SYMPTOMS:
            x[0, SYMPTOMS.index(s)] = 1

    probs = MODEL.predict_proba(x)[0]
    idx = np.argsort(probs)[-3:][::-1]

    diseases = ENCODER.inverse_transform(idx)
    conf = (probs[idx] * 100).round(2)

    table = [{"Disease": d, "Confidence": float(c)} for d, c in zip(diseases, conf)]

    fig = px.bar(
        x=diseases,
        y=conf,
        labels={"x": "Disease", "y": "Confidence (%)"},
        text=conf,
        range_y=[0, 100],
    )
    fig.update_layout(template="plotly_white")

    chart = json.dumps(fig, cls=PlotlyJSONEncoder)

    details = None

    ml_name = diseases[0].strip().lower()
    mapping = DISEASE_NAME_MAPPING.get(ml_name)

    primary_name = None
    related_conditions = []

    if mapping:
        if isinstance(mapping, dict):
            primary_name = mapping["primary"]
            related_conditions = mapping.get("related", [])
        else:
            primary_name = mapping

    if primary_name:
        lookup_key = primary_name.strip().lower()

        if lookup_key in HEALTH_DF.index:
            row = HEALTH_DF.loc[lookup_key]

            sections = [
                "Overview",
                "Symptoms",
                "When to see a doctor",
                "Causes",
                "Risk factors",
                "Complications",
                "Prevention",
                "Diagnosis",
                "Treatment",
                "Coping and support",
                "Preparing for your appointment",
                "Lifestyle and home remedies",
            ]

            details = {
                "title": primary_name,
                "main_link": safe_value(row.get("main_link")),
                "diagnosis_treatment_link": safe_value(
                    row.get("Diagnosis_treatment_link")
                ),
                "doctors_departments_link": safe_value(
                    row.get("Doctors_departments_link")
                ),
                "sections": {sec: safe_value(row.get(sec)) for sec in sections},
                "last_updated": safe_value(row.get("updated")),
                "related_conditions": related_conditions,
            }

    return jsonify({"table": table, "confidence_chart": chart, "details": details})


@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({"error": "API limit exceeded. Please try again later."}), 429


if __name__ == "__main__":
    app.run()