
from datetime import datetime
from typing import Optional

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

app = FastAPI(title="AGENTRA SalonFlow")

# Demo data only. Replace with the salon's verified details.
SALON = {
    "name": "Glow Studio",
    "services": {
        "haircut": 500,
        "facial": 999,
        "manicure": 399,
        "hair spa": 799,
    },
    "hours": "10:00 AM to 8:00 PM",
}

# Temporary storage: requests disappear when the server restarts.
booking_requests = []


class ChatMessage(BaseModel):
    message: str = Field(min_length=1, max_length=1000)


class BookingRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    phone: str = Field(min_length=7, max_length=20)
    service: str = Field(min_length=1, max_length=100)
    date: str = Field(min_length=1, max_length=30)
    time: str = Field(min_length=1, max_length=30)


@app.get("/")
def home():
    return FileResponse("index.html")


@app.get("/api/health")
def health():
    return {"status": "ok", "app": "AGENTRA SalonFlow"}


@app.post("/api/chat")
def chat(data: ChatMessage):
    message = data.message.lower().strip()

    if any(word in message for word in ["hi", "hello", "hey"]):
        reply = (
            f"Hi! Welcome to {SALON['name']} ✨ "
            "I can help with services, prices, opening hours, "
            "and booking requests. What would you like to know?"
        )

    elif any(word in message for word in ["price", "cost", "charge", "rate"]):
        prices = "\n".join(
            f"• {service.title()}: ₹{price}"
            for service, price in SALON["services"].items()
        )
        reply = f"Here is our demo price list:\n{prices}"

    elif any(word in message for word in ["service", "offer", "available"]):
        reply = (
            "Our demo services are haircut, facial, manicure, "
            "and hair spa. Ask me for prices or request a booking."
        )

    elif any(word in message for word in ["hour", "open", "timing", "close"]):
        reply = f"Our demo opening hours are {SALON['hours']}."

    elif any(word in message for word in ["book", "appointment", "slot"]):
        reply = (
            "I'd be happy to help! Fill in the booking request form "
            "below. The salon owner must confirm your requested slot."
        )

    elif any(word in message for word in ["thank", "thanks"]):
        reply = "You're welcome! ✨ Is there anything else I can help with?"

    else:
        reply = (
            "I can help with our demo services, prices, opening hours, "
            "and booking requests. What would you like to know?"
        )

    return {"reply": reply, "mode": "demo"}


@app.post("/api/bookings")
def create_booking(data: BookingRequest):
    booking = data.model_dump()
    booking["created_at"] = datetime.now().isoformat(timespec="seconds")
    booking["status"] = "Pending salon confirmation"

    booking_requests.append(booking)

    return {
        "message": "Booking request received! The salon must confirm "
                   "your appointment.",
        "booking": booking,
    }


@app.get("/api/bookings")
def list_bookings():
    # Demo/admin endpoint; do not expose publicly in production.
    return {"bookings": booking_requests}
