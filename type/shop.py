import hashlib
from datetime import datetime, date
from typing import Any, Union, Literal

import typing_extensions
from pydantic import BaseModel, ConfigDict, Field
from fastapi import Form, UploadFile, File

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

class add_shop_interface(BaseModel):
    address: str = Form(None)
    name: str = Form(None)
    user_id: int = 0
    photo: UploadFile = File(None)

class order_interface(BaseModel):
    order_list: list = None

class pro_update(BaseModel):
    product_id: int = Form(None)
    price:float = Form(None)
    name: str = Form(None)
    description: str = Form(None)
    shop_id: int = Form(None)
    stock: int = Form(None)
    image: UploadFile = File(None)