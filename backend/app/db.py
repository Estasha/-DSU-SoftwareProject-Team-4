"""데이터베이스 연결 설정 (Turso libSQL)"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    # Supabase 접속 정보가 없으면 로컬 SQLite로 폴백 (로컬 테스트용)
    DATABASE_URL = "sqlite:///./test.db"

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """FastAPI 의존성 주입용: 요청마다 DB 세션을 열고 끝나면 닫음"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
