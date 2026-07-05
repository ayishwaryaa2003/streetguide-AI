from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.routes import router

app = FastAPI(title="StreetGuide AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API
app.include_router(router)

# Static frontend
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")


@app.get("/")
async def home():
    return FileResponse("frontend/index.html")