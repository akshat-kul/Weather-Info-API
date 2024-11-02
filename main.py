from fastapi import FastAPI
import uvicorn
from weather_info.routers import weather_info_router

app = FastAPI(
    title="Weather Info API",
)

app.include_router(weather_info_router, prefix="/weather_info")

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)

