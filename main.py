import datetime
import jwt
import time
import models
import os
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from korean_lunar_calendar import KoreanLunarCalendar
from typing import List, Annotated
from sqlalchemy.orm import Session
from uuid import uuid4
from starlette.middleware.cors import CORSMiddleware
from database import engine, SessionLocal
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
models.Base.metadata.create_all(bind=engine)

dates = [
    ['새해', '2024-01-01', False],
    ['설날', '2024-01-01', True],
    ['추석', '2024-08-15', True]
]

session = SessionLocal()
result = session.query(models.Check_Date).all()

for day in dates:
    is_it = False
    for rs in result:
        if rs.name == day[0]:
            is_it = True
    if not is_it:
        check_date = models.Check_Date(id=uuid4(), name=day[0], date=day[1], is_korean_luna=day[2])
        session.add(check_date)

session.commit()

session.close()


class UserBase(BaseModel):
    name: str
    token: str


calendar = KoreanLunarCalendar()

now = datetime.datetime.now()
year = now.year
month = now.month
day = now.day

calendar.setSolarDate(year, month, day)

lunar_now = calendar.LunarIsoFormat()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


def create_user(user: UserBase, db: db_dependency):
    db_users = models.Users(name=user.name, token=user.token)
    db.add(db_users)
    db.commit()
    db.refresh(db_users)


def login_user(user: UserBase, db: db_dependency):
    db_users = db.query(models.Users).filter(models.Users.name == user.name, models.Users.token == user.token).one()
    # 사용자가 있는지 확인
    print(db_users)
    # 없으면 에러
    # 있다면 엑세스 토큰과 리프레쉬 토큰 발급


def encoding(id: str, token: str, date: int):
    private_key = os.getenv('SECRET_KEY')
    algorithm = 'RS256'
    now = time.time()
    day_second = 86400
    payload = {
        "iss": os.getenv('ROOT'),
        "exp": now + (day_second * date),
        "iat": now,
        "id": id,
        "token": token
    }
    json_web_token = jwt.encode(payload, private_key, algorithm=algorithm)
    print(json_web_token)
    return json_web_token


def decoding(token: str):
    public_key = os.getenv('PUBLIC_KEY')
    algorithm = 'RS256'
    print(jwt.decode(token, public_key, algorithms=algorithm))


jwt_token = encoding(id="1", date=2)
decoding(jwt_token)
