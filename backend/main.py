from fastapi import FastAPI
from booli_route import booli

app = FastAPI(title="House Search",debug=True)
app.include_router(booli.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

