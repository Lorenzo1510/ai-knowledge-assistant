from fastapi import FastAPI, UploadFile, File
import uvicorn


app = FastAPI()


@app.get("/")
def health_check():
    return {"status": "ok"}


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    # TODO: estrai testo e indicizza
    return {"message": f"File '{file.filename}' uploaded successfully"}


@app.post("/ask")
async def ask_question(question: str):
    # TODO: recupera documenti e genera risposta
    return {"answer": "This is a placeholder answer"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
