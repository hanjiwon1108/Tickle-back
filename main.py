from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from src.interfaces.api import auth, chat, analysis, public_data, assets, transactions, notifications

load_dotenv()

app = FastAPI(title="Tickle API", description="Backend for Tickle - AI Financial Advisor")

app.include_router(auth.router)
app.include_router(chat.router)
app.include_router(analysis.router)
app.include_router(public_data.router)
app.include_router(assets.router)
app.include_router(transactions.router)
app.include_router(notifications.router)

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to Tickle API"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
