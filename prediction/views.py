from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import numpy as np
import xgboost as xgb
import os

# ✅ Load the trained XGBoost model
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "prediction", "models", "student_depression_xgb_model.json")

xgb_model = xgb.Booster()
try:
    xgb_model.load_model(MODEL_PATH)
    print("✅ Model loaded successfully!")
except Exception as e:
    print("❌ Error loading model:", str(e))

# ✅ Home page function
from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, "predict.html")  # ✅ Renders the home page

# ✅ Test if Django can detect this view
def test_home(request):
    return HttpResponse("✅ Home view is working!")  # Simple text response for debugging

import pandas as pd


# ✅ Column names used in training
COLUMN_NAMES = [
    "Academic Pressure",
    "Study Satisfaction",
    "Sleep Duration",
    "Dietary Habits",
    "Have you ever had suicidal thoughts ?",
    "Work/Study Hours",
    "Financial Stress",
    "Family History of Mental Illness"
]

@csrf_exempt
def predict_depression(request):
    if request.method == "POST":
        try:
            print("✅ Received a request")
            
            if request.content_type != "application/json":
                return JsonResponse({"error": "Invalid content type. Use application/json"}, status=400)

            data = json.loads(request.body)
            print("📩 Parsed JSON Data:", data)

            if "features" not in data:
                return JsonResponse({"error": "Missing 'features' key in request"}, status=400)
            
            # ✅ Convert input list to Pandas DataFrame
            input_df = pd.DataFrame([data["features"]], columns=COLUMN_NAMES)
            print("📊 DataFrame Input:\n", input_df)

            # ✅ Convert to XGBoost DMatrix
            dmatrix = xgb.DMatrix(input_df)

            # ✅ Make prediction (0 or 1)
            prediction = int(round(xgb_model.predict(dmatrix)[0]))
            print("🔮 Raw Prediction:", prediction)

            # ✅ Map prediction to meaningful text
            result_text = "The student is likely in depression." if prediction == 1 else "The student is NOT in depression."

            return JsonResponse({"prediction": prediction, "message": result_text}, status=200)

        except Exception as e:
            print("❌ Error:", str(e))
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Only POST requests are allowed"}, status=405)

