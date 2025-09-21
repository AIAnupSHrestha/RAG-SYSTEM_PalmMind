from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime, timezone

DATABASE_URL = "sqlite:///./RAG_data.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
session = sessionmaker(autocommit= False, autoflush=False, bind=engine)

Base = declarative_base()

class Bookings(Base):
    __tablename__ = "Bookings"
    id = Column(Integer, primary_key = True, index = True)
    name = Column(String, nullable=False)
    date = Column(String, nullable=False)
    time = Column(String, nullable=False)

class MetaData(Base):
    __tablename__ = "MetaData"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    chunking_strategy = Column(String, nullable=False)
    weaviate_id = Column(String, nullable=False)
    chunk_length = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


Base.metadata.create_all(bind=engine)

def saveBooking(data: dict) -> None:
    db = session()
    booking = Bookings(**data)
    db.add(booking)
    db.commit()
    db.close()

def getBookings():
    db = session()
    bookings = db.query(Bookings).all()
    db.close()
    return bookings

def saveMetaData(filename: str, chunking_strategy: str, weaviate_id: str, chunk_length: int):
    db = session()
    metadata = MetaData(
        filename=filename,
        chunking_strategy=chunking_strategy,
        weaviate_id=weaviate_id,
        chunk_length=chunk_length
    )
    db.add(metadata)
    db.commit()
    db.close()

def getMetaData():
    db = session()
    metadata = db.query(MetaData).all()
    db.close()
    return metadata
    