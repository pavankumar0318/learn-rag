import os
from fastapi import FastAPI, UploadFile, File, Request
from EmbedService import PDFEmbedService
from PIIGuard import mask_pii

app = FastAPI(title="LoanIQ RAG API")

pdf_embed_service = PDFEmbedService()

UPLOAD_DIR = "./uploaded_pdfs"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.post("/upload_pdf")
async def upload_pdf(file: UploadFile = File(...)):
    content = await file.read()
    pdf_embed_service.save_and_embed(file.filename, content)
    return {"message": f"'{file.filename}' uploaded and indexed successfully."}


@app.post("/query")
async def query_rag(request: Request):
    data       = await request.json()
    user_query = data.get("query", "").strip()

    if not user_query:
        return {"error": "No query provided."}

    # Mask PII before sending to the RAG pipeline
    safe_query = mask_pii(user_query)
    result     = pdf_embed_service.rag_service.invoke_rag(safe_query)

    # Mask PII in the answer before returning
    result["answer"] = mask_pii(result.get("answer", ""))

    return {"result": result}