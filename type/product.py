import hashlib
from datetime import datetime, date
from typing import Any, Union

from fastapi import UploadFile, File
from pydantic import BaseModel, ConfigDict, Field

class product_add_interface(BaseModel):
    name: str
    description: str
    price: float
    category: str
    shop_id : int
    stock : int
    image : str

    # 可以根据需要添加更多字段，如库存量、商品图片等
class ProductRequest(BaseModel):
    token: str
    id: int

class ProductSearch(BaseModel):
    name: str

class ProductBuy(BaseModel):
    token: str
    pro_id : int
    user_id : int
    number : int

class comment_add(BaseModel):
    token: str
    product_id : int
    user_id : int
    review : str


class add_product(BaseModel):
    image: UploadFile = File(...)
    description: str = Field(..., strip_whitespace=True, min_length=1)
    price: float = Field(..., gt=0)
    name: str = Field(..., strip_whitespace=True, min_length=1)
    shop_id: int = Field(..., gt=0)
    stock: int = Field(..., gt=0)

