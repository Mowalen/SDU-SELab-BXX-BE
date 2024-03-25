import hashlib
from datetime import datetime, date
from typing import Any, Union
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

