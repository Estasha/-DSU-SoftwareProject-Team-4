"""데이터베이스 연결 설정 (Turso libSQL)"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL이 .env에 설정되어 있지 않습니다. backend/.env.example 참고")

# sqlalchemy-libsql 드라이버는 URL 쿼리스트링의 authToken을 인식하지 못해서
# connect_args로 따로 넘겨줘야 함 (안 그러면 "empty JWT token" 에러 발생)
_url = make_url(DATABASE_URL)
_auth_token = _url.query.get("authToken")
if _auth_token:
    _url = _url.difference_update_query(["authToken"])

engine = create_engine(_url, connect_args={"auth_token": _auth_token} if _auth_token else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """FastAPI 의존성 주입용: 요청마다 DB 세션을 열고 끝나면 닫음"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
