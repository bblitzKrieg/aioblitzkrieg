from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict


class Archive(BaseModel):

    id: int
    status: str
    add_dt: datetime

class ArchiveList(BaseModel):

    results: List[Archive]
    total_count: int

class ArchiveReport(BaseModel):

    status: str
    account_results: Dict[str, int]
    total_accounts: int
    purchase_results: Dict[str, int]
    total_purchases: int