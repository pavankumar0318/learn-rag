from fastapi import FastAPI, UploadFile, File, Request
from EmbedService import PDFEmbedService
import os

app = FastAPI()
pdf_embed_service = PDFEmbedService()

UPLOAD_DIR = "./uploaded_pdfs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload_pdf")
async def upload_pdf(file: UploadFile = File(...)):
    content = await file.read()
    pdf_embed_service.save_and_embed(file.filename, content)
    return {"message": "PDF uploaded and indexed successfully."}

@app.post("/query")
async def query_rag(request: Request):
    data = await request.json()
    user_query = data.get("query", "")
    if not user_query:
        return {"error": "No query provided."}
    result = pdf_embed_service.rag_service.invoke_rag(user_query)
    return {"result": result}

# To run: uvicorn api_rag_service:app --reload
