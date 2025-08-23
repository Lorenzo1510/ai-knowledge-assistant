import os

from fastapi import APIRouter, UploadFile, File

from app.utils.pdf_parser import extract_text_from_pdf
from app.services.rag_service import index_document


router = APIRouter()
UPLOAD_DIR = "data/uploaded_files"

@router.post("/upload/")
async def upload_pdf(file: UploadFile = File(...)):
    content = await file.read()
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    with open(f"{UPLOAD_DIR}/{file.filename}", "wb") as f:
        f.write(content)

    text = extract_text_from_pdf(f"{UPLOAD_DIR}/{file.filename}")
    index_document(text, file.filename)
    
    return {"message": f"File '{file.filename}' uploaded successfully", "text": text}