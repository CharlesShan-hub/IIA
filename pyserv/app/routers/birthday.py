from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import SessionLocal
from app.models.birthday import Birthday
from datetime import date

router = APIRouter()

# 依赖函数，用于获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 新增生日记录
@router.post("/birthdays/")
def create_birthday(name: str, birthdate: date, db: Session = Depends(get_db)):
    birthday = Birthday(name=name, birthdate=birthdate)
    db.add(birthday)
    db.commit()
    db.refresh(birthday)
    return birthday

# 获取所有生日记录
@router.get("/birthdays/")
def read_all_birthdays(db: Session = Depends(get_db)):
    birthdays = db.query(Birthday).all()
    return birthdays

# 根据ID获取生日记录
@router.get("/birthdays/{birthday_id}")
def read_birthday(birthday_id: int, db: Session = Depends(get_db)):
    birthday = db.query(Birthday).filter(Birthday.id == birthday_id).first()
    return birthday

# 更新生日记录
@router.put("/birthdays/{birthday_id}")
def update_birthday(birthday_id: int, name: str, birthdate: date, db: Session = Depends(get_db)):
    birthday = db.query(Birthday).filter(Birthday.id == birthday_id).first()
    if birthday:
        birthday.name = name
        birthday.birthdate = birthdate
        db.commit()
        db.refresh(birthday)
    return birthday

# 删除生日记录
@router.delete("/birthdays/{birthday_id}")
def delete_birthday(birthday_id: int, db: Session = Depends(get_db)):
    birthday = db.query(Birthday).filter(Birthday.id == birthday_id).first()
    if birthday:
        db.delete(birthday)
        db.commit()
    return {"message": "Birthday record deleted successfully"}