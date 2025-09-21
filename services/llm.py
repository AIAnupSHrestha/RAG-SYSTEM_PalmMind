from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from typing import List, Dict, Optional
import os, re, torch
from models.booking_model import Booking
from huggingface_hub import login
from dotenv import load_dotenv

os.environ["TRANSFORMERS_VERBOSITY"] = "info"
load_dotenv() 

login(os.getenv("HUGGINGFACE_TOKEN"))

MODEL_NAME = "meta-llama/Llama-3.2-1B-Instruct"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    device_map="auto",
    dtype=torch.float16,
    low_cpu_mem_usage=True
)

llm_pipeline = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=150,        
    do_sample=True,            
    temperature=0.4,           
    top_k=40,                  
    top_p=0.85,                
    repetition_penalty=1.2,    
    pad_token_id=tokenizer.eos_token_id
)

def generate_response(query: str, docs: List[Dict], history: List[Dict]) -> str:
    messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

    # if history:
    #     messages.extend([{"role": conv['role'], "content": conv['message']} for conv in history])

    # context = "\n".join([doc.get("text", "") for doc in docs])

    # messages.append({
    #     "role": "user",
    #     "content": f"""
    #     User requested: {query}

    #     Relevant Context:
    #     {context}

    #     Generate a clear, concise, and user-friendly response. 
    #     Start directly with the answer to the user's request, without adding greetings, signatures, 
    #     or unnecessary text. Keep the tone professional yet approachable.
    #     """
    # })


    context = "\n".join([doc.get("text", "") for doc in docs])
    history_text = "\n".join([f"{conv['role']}: {conv['message']}" for conv in history]) if history else ""

    # Build final prompt
    prompt = f"""
    You are a helpful assistant.

    Conversation History:
    {history_text}

    User requested: {query}

    Relevant Context:
    {context}

    Generate a clear, concise, professional, and user-friendly response. 
    Start directly with the answer, without greetings or unnecessary text.
    """

    # response = llm_pipeline(prompt)

    # if response and response[0].get("generated_text"):
    #     generated_messages = response[0]["generated_text"]
    #     if generated_messages and isinstance(generated_messages, list) and generated_messages[-1].get("role") == "assistant":
    #         return generated_messages[-1]["content"].strip()

    with torch.no_grad():
        response = llm_pipeline(
            prompt
        )

    # HF pipeline returns a list of dicts with "generated_text"
    if response and "generated_text" in response[0]:
        return response[0]["generated_text"].strip()

    return "Sorry, I could not generate a response."


def detect_booking(query: str) -> Optional[Booking]:
    if not any(kw in query.lower() for kw in ["book", "schedule", "appointement"]):
        return None  

    name_match = re.search(r'with\s+([A-Za-z ]+?)\s+at', query)
    name = name_match.group(1).strip() if name_match else None

    time_match = re.search(r'at\s+([0-9apm: ]+)\s+on', query)
    time = time_match.group(1).strip() if time_match else None

    date_match = re.search(r'on\s+([0-9a-zA-Z ]+)', query)
    date = date_match.group(1).strip() if date_match else None

    print(name_match, date_match, time_match)

    if name and time and date:
        return {
            "name": name,
            "time": time,
            "date": date,
        }
    return None

def generate_booking_response(
        query: str,
        booking: Booking,
        history: Optional[List[Dict]] = None
) -> str:
    
    print(query)
    
    messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]
    if history:
        messages.extend([{"role": conv['role'], "content": conv['message']} for conv in history])
    
    messages.append({
        "role": "user",
        "content": f"""
        User requested a booking: {query}
        
        Booking details:
        - Name: {booking["name"]}
        - Date: {booking["date"]}
        - Time: {booking["time"]}
        
        Generate a friendly confirmation message starting with "Thank you for requesting an interview with us! 
        We've confirmed your appointment with {booking['name']} for {booking['time']} on {booking['date']}." Followed by "If you have 
        any questions or need any further assistance, please don't hesitate to reach out." Do not add greetings, 
        quotes, signatures, or any other text.
        """
    })

    response = llm_pipeline(messages)
    if response and response[0].get("generated_text"):
        generated_messages = response[0]["generated_text"]
        if generated_messages and isinstance(generated_messages, list) and generated_messages[-1].get("role") == "assistant":
            return generated_messages[-1]["content"].strip()
    
    return "Sorry, I could not generate a response."