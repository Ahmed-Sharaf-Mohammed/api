from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy import create_engine, Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import shutil
import os
import uuid

app = FastAPI()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

DATABASE_URL = "sqlite:///./uploads.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# تعديل الجدول لاضافة user_id
class Upload(Base):
    __tablename__ = "uploads"
    file_id = Column(String, primary_key=True, index=True)
    filename = Column(String)
    link = Column(String)
    timestamp = Column(DateTime)
    user_id = Column(String)  # إضافة حقل user_id

Base.metadata.create_all(bind=engine)

# تعديل دالة رفع الصورة لتستقبل user_id
@app.post("/upload/")
async def upload_image_and_link(
        file: UploadFile = File(...),
        link: str = Form(...),
        user_id: str = Form(...)  # إضافة user_id كـ Form
):
    file_id = f"{uuid.uuid4().hex}_{file.filename}"
    filepath = os.path.join(UPLOAD_FOLDER, file_id)

    # حفظ الملف
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # حفظ البيانات في قاعدة البيانات مع user_id
    db = SessionLocal()
    new_upload = Upload(
        file_id=file_id,
        filename=file.filename,
        link=link,
        timestamp=datetime.utcnow(),
        user_id=user_id  # حفظ user_id مع باقي البيانات
    )
    db.add(new_upload)
    db.commit()
    db.close()

    return {"message": "Uploaded successfully", "id": file_id}

# 1. مسار جلب البيانات الكاملة
@app.get("/get/{user_id}")
def get_uploaded_data(user_id: str):
    db = SessionLocal()
    data = db.query(Upload).filter(Upload.user_id == user_id).all()  # استخدام user_id في البحث
    db.close()

    if not data:
        raise HTTPException(status_code=404, detail="No files found for this user")

    return [
        {
            "file_id": item.file_id,
            "filename": item.filename,
            "link": item.link,
            "uploaded_at": item.timestamp.isoformat(),
            "user_id": item.user_id
        }
        for item in data
    ]

# 2. مسار جلب الصور فقط
@app.get("/image/{user_id}")
def get_images(user_id: str):
    db = SessionLocal()
    data = db.query(Upload).filter(Upload.user_id == user_id).all()  # استخدام user_id في البحث
    db.close()

    if not data:
        raise HTTPException(status_code=404, detail="No images found for this user")

    return [
        {
            "image_url": f"/image/{item.file_id}",
        }
        for item in data
    ]

# 3. مسار جلب الروابط فقط
@app.get("/link/{user_id}")
def get_links(user_id: str):
    db = SessionLocal()
    data = db.query(Upload).filter(Upload.user_id == user_id).all()  # استخدام user_id في البحث
    db.close()

    if not data:
        raise HTTPException(status_code=404, detail="No links found for this user")

    return [
        {
            "link": item.link,
        }
        for item in data
    ]

# 4. مسار جلب وقت الرفع فقط
@app.get("/time/{user_id}")
def get_time(user_id: str):
    db = SessionLocal()
    data = db.query(Upload).filter(Upload.user_id == user_id).all()  # استخدام user_id في البحث
    db.close()

    if not data:
        raise HTTPException(status_code=404, detail="No timestamps found for this user")

    return [
        {
            "uploaded_at": item.timestamp.isoformat(),
        }
        for item in data
    ]

# دالة عرض الصورة بناءً على file_id
@app.get("/image/{file_id}")
def get_image(file_id: str):
    db = SessionLocal()
    data = db.query(Upload).filter(Upload.file_id == file_id).first()
    db.close()

    if not data:
        raise HTTPException(status_code=404, detail="File not found")

    filepath = os.path.join(UPLOAD_FOLDER, data.file_id)
    return FileResponse(filepath)
