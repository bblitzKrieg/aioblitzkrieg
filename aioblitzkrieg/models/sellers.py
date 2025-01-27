from pydantic import BaseModel


class Seller(BaseModel):

    id: int
    telegram_id: int
    balance: float
    language: str

class SellerShortApi(BaseModel):

    id: int
    telegram_id: int
    api_key: str

class SellerShort(BaseModel):

    id: int
    telegram_id: int