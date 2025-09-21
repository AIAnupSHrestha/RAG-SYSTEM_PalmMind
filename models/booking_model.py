from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class Booking(BaseModel):
    name: str = Field(..., description="Person to book")
    time: str = Field(..., description="Booking time")
    date: str = Field(..., description="Booking date")
    email: EmailStr = Field(..., description="Email of the person booking")