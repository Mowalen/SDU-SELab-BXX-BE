import hashlib
from datetime import datetime, date
from typing import Any, Union, Literal, Optional

import typing_extensions
from fastapi import UploadFile, File, Form
from pydantic import BaseModel, ConfigDict, Field


class login_interface(BaseModel): # 登陆时使用
    username: str = None
    password: str = None
    type: int = None

class register_interface(login_interface): # 注册时使用
    username: str = None
    password: str = None
    type: int = None

class user_edit_interface(register_interface): # 用户登录成功后修改个人信息
    address: str = Form(None)
    phone: str = Form(None)
    id_card_number: str = Form(None)
    photo: UploadFile = File(None)
    token: str = None

class user_add_interface(BaseModel): # 向数据库中加入个人信息
    id: str = None
    username: str = None
    password: str = None
    type: str = None
    has_delete: str = None

class session_interface(BaseModel): # 用于token缓存
    user_id: int
    file_id: int = None
    token: str
    use: int = 0
    token_s6: str = None
    use_limit: int = None
    exp_dt: int
    ip: str
    user_agent: str
    func_type: int

class order_interface(BaseModel): # 用于返回商品订单详情
    shop_name: str = None
    status: int = 0
    amount: float = 0.0
    quantity: int = 0
    name: str = None
    photo: str = None
    address: str = None
    order_id: int = 0
    shop_id: int = 0
    product_id: int = 0
    time: datetime = None

class shop_interface(BaseModel): # 用于返回店铺详情
    shop_name: str = None
    sales_volume: int = 0
    address: str = None
    photo: str = None
    time: str = None
    order: list = []

class shop_id_interface(BaseModel): #用户返回店铺id
    id: int = 0

class shop_create_interface(BaseModel): #商家创建店铺
    address: str = Form(None)
    name: str = Form(None)
    user_id: int = 0
    photo: UploadFile = File(None)