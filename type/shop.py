import hashlib
from datetime import datetime, date
from typing import Any, Union, Literal

import typing_extensions
from pydantic import BaseModel, ConfigDict, Field


class shop_request(BaseModel):
    token: str = None
    id: int = None

class search_shop(BaseModel):
    token: str = None
    temp: str = None

class shop_updata(BaseModel):
    token: str = None
    name: str = None
    user_id: int = None
    owner_name: str = None


class add_shop(BaseModel):
    name: str = None
    user_id: int = None
    owner_name: str = None