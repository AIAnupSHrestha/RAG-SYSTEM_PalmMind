from fastapi import APIRouter, HTTPException
from models.rag_model import RAGQuery
from services.weaviate_client import query_weaviate
from services.llm import generate_response, detect_booking, generate_booking_response
from services.RedisMemory import save_message, get_conversation
from services.database import saveBooking
from models.booking_model import Booking
router = APIRouter()

@router.post("/query")
async def rag_query(payload: RAGQuery):
    try:
        history = get_conversation(session_id=payload.session_id)

        booking_data = detect_booking(query=payload.query)

        if booking_data:
            saveBooking(Booking(**booking_data).model_dump())
            response = generate_booking_response(query=payload.query, booking=booking_data, history=history)
            save_message(session_id=payload.session_id, role="user", message=payload.query)
            save_message(session_id=payload.session_id, role="assistant", message=payload.query)

            return {"response": response, "docs": []}
        
        docs = query_weaviate(payload.query)
        answer = generate_response(payload.query, docs, history)
        save_message(payload.session_id, "user", payload.query)
        save_message(payload.session_id, "assistant", answer)

        return {"answer": answer, "docs": docs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))