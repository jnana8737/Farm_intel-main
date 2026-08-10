from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from utils import full_system

app = FastAPI()

# 🔥 CORS (frontend connection)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CropRequest(BaseModel):
    district: str = None
    lat: float = None
    lon: float = None
    season: str
    mode: str
    N: float = None
    P: float = None
    K: float = None

@app.get("/")
def home():
    return {"message": "AgroSmart AI Backend Running 🚀"}

@app.post("/predict")
def predict(data: CropRequest):
    return full_system(
        lat=data.lat,
        lon=data.lon,
        district=data.district,
        season=data.season,
        mode=data.mode,
        N=data.N,
        P=data.P,
        K=data.K
    )