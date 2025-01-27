from typing import Dict, Union
from pydantic import BaseModel


class Prices(BaseModel):
    prices: Dict[str, Dict[str, Union[int, float]]]