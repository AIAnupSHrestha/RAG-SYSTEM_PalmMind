from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class Booking(BaseModel):
    # session_id: str = Field(..., description="User session ID")
    name: str = Field(..., description="Person to book")
    time: str = Field(..., description="Booking time")
    date: str = Field(..., description="Booking date")
    # created_at: datetime = Field(default_factory=datetime.utcnow, description="Booking creation timestamp")