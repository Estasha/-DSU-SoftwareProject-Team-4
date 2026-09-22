"""데이터베이스 연결 설정 (Turso libSQL / 로컬 SQLite 폴백)"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    # Turso 접속 정보가 없으면 로컬 SQLite 파일로 폴백 (로컬 테스트용)
    DATABASE_URL = "sqlite:///./test.db"

# 로컬 SQLite 파일 연결에서만 필요한 옵션 (Turso/libSQL 원격 연결에는 불필요)
is_local_sqlite_file = DATABASE_URL.startswith("sqlite:///")
connect_args = {"check_same_thread": False} if is_local_sqlite_file else {}
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
