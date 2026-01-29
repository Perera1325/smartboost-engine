from fastapi import FastAPI
from routes import router

app = FastAPI(title="SmartBoost Engine")

app.include_router(router)

@app.get("/")
def root():
    return {"message": "SmartBoost Engine is running"}
