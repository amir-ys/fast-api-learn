from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal, init_db
from app.models import Fact

app = FastAPI()

@app.on_event("startup")
def startup():
    init_db()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/fact/{fact_id}")
async def get_fact(fact_id: int, db: Session = Depends(get_db)):
    fact = db.query(Fact).filter(Fact.id == fact_id).first()
    if not fact:
        return {"error": "Fact not found"}
    return {"fact_id": fact.id, "fact": fact.text}


# API برای اضافه کردن واقعیت
@app.post("/fact/", response_model=FactResponse, status_code=201)
async def create_fact(fact: FactCreate, db: Session = Depends(get_db)):
    # بررسی تکراری بودن واقعیت
    existing_fact = db.query(Fact).filter(Fact.text == fact.text).first()
    if existing_fact:
        raise HTTPException(status_code=400, detail="Fact already exists")
    
    # ایجاد و ذخیره واقعیت جدید
    new_fact = Fact(text=fact.text)
    db.add(new_fact)
    db.commit()
    db.refresh(new_fact)
    return new_fact
