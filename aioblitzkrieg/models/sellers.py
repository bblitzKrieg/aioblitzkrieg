from pydantic import BaseModel


class Seller(BaseModel):

    id: int
    telegram_id: int
    balance: float
    language: str