from sqlalchemy import create_engine, Column, String, Float, DateTime, Integer
from sqlalchemy.orm import declarative_base, sessionmaker
from config import DATABASE_URL

# Create engine & session factory
engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

# Table for dose + glucose events
class Dose(Base):
    __tablename__ = "doses"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String, index=True)
    timestamp = Column(DateTime, index=True)
    dosage_units = Column(Float)
    carbs_g = Column(Float)
    glucose_mgdl = Column(Float)
    meal_tag = Column(String, nullable=True)

def init_db():
    """Initialize database tables."""
    Base.metadata.create_all(bind=engine)
