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

class shop_updata(BaseModel):
    name : str
    user_id : id
    owner_name : str

class add_shop(BaseModel):
    name : str
    user_id : id
    owner_name : str