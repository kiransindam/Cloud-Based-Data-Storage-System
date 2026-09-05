from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.document import Document
from app.schemas.document import DocumentOut
from app.services.storage import storage

router = APIRouter(prefix="/documents", tags=["documents"])

MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB
ALLOWED_TYPES = {
    "application/pdf", "image/jpeg", "image/png", "image/gif",
    "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "text/plain", "application/zip",
}


@router.post("/", response_model=DocumentOut, status_code=201)
async def upload_document(
    file: UploadFile = File(...),
    tags: str = Query("", description="Comma-separated tags"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(400, f"File type {file.content_type} not allowed")

    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(413, f"File too large. Max {MAX_FILE_SIZE // (1024*1024)}MB")

    # Reset file pointer for storage service
    await file.seek(0)
    result = await storage.upload(current_user.id, file)

    doc = Document(
        owner_id=current_user.id,
        filename=file.filename,
        s3_key=result["s3_key"],
        content_type=file.content_type,
        size_bytes=result["size_bytes"],
        tags=tags,
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc


@router.get("/", response_model=list[DocumentOut])
def list_documents(
    search: str = Query("", description="Search filename or tags"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Document).filter(Document.owner_id == current_user.id)
    if search:
        pattern = f"%{search}%"
        query = query.filter(
            (Document.filename.ilike(pattern)) | (Document.tags.ilike(pattern))
        )
    docs = query.order_by(Document.created_at.desc()).all()

    results = []
    for d in docs:
        out = DocumentOut.model_validate(d)
        out.download_url = storage.generate_presigned_url(d.s3_key)
        results.append(out)
    return results


@router.get("/{doc_id}", response_model=DocumentOut)
def get_document(doc_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    doc = db.query(Document).filter(Document.id == doc_id, Document.owner_id == current_user.id).first()
    if not doc:
        raise HTTPException(404, "Document not found")
    out = DocumentOut.model_validate(doc)
    out.download_url = storage.generate_presigned_url(doc.s3_key)
    return out


@router.delete("/{doc_id}", status_code=204)
def delete_document(doc_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    doc = db.query(Document).filter(Document.id == doc_id, Document.owner_id == current_user.id).first()
    if not doc:
        raise HTTPException(404, "Document not found")
    storage.delete(doc.s3_key)
    db.delete(doc)
    db.commit()
