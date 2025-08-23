from fastapi import FastAPI, UploadFile, File
import uvicorn
from app.api.routes import router


app = FastAPI()
app.include_router(router)


@app.get("/")
def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
