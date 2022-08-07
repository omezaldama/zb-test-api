import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.dependencies.database import get_db
from app.utils.database import Base


TEST_SQLALCHEMY_DATABASE_URL = "sqlite:///./test_sql_app.db"
test_engine = create_engine(
    TEST_SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def test_db():
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)

app.dependency_overrides[get_db] = override_get_db
