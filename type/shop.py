import hashlib
from datetime import datetime, date
from typing import Any, Union
from pydantic import BaseModel, ConfigDict, Field


class shop_request(BaseModel):
    token : str
    id : int

class search_shop(BaseModel):
    token : str
    temp : str