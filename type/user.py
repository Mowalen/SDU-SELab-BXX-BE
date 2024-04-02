import hashlib
from datetime import datetime, date
from typing import Any, Union, Literal

import typing_extensions
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
    address: str = None
    phone: str = None
    id_card_number: str = None
    photo: str = None
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
    status: str = None
    amount: str = None
    quantity: str = None
    name: str = None
    photo: str = None
    address: str = None