from pydantic import BaseModel


class StatusMessageSchema(BaseModel):
    text: str
    status_id: int
    order_id: int
