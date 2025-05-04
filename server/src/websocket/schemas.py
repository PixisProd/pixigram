from pydantic import BaseModel


class WSMessage(BaseModel):
    text: str
    is_system: bool
    sender_id: int