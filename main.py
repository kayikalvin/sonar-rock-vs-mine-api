from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import joblib

app = FastAPI()
# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change "*" to your frontend URL for better security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Load the trained model
model = joblib.load("model.pkl")

# Define the request body structure
class ModelInput(BaseModel):
    features: list[float]  # Adjust based on your model's input shape


@app.get('/')
def home():
    return {'message': 'FastAPI running'}

@app.post("/predict")
def predict(data: ModelInput):
    features = np.array(data.features).reshape(1, -1)  # Ensure correct shape
    prediction = model.predict(features).tolist()
    return {"prediction": prediction}

# Run the API with: uvicorn main:app --host 0.0.0.0 --port 8000
