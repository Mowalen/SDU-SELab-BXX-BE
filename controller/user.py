import datetime
import json
import random
import string
import uuid
from pydantic import main
from fastapi import APIRouter, HTTPException,FastAPI
from fastapi import Request, Header, Depends
from model.db import session_db, user_information_db
from service.user import UserModel, SessionModel, UserinfoModel, OperationModel, CaptchaModel
from type.user import user_info_interface, \
    session_interface, email_interface, password_interface, user_add_interface, admin_user_add_interface, \
    login_interface, \
    captcha_interface, user_interface, reason_interface, user_add_batch_interface, oj_login_interface
from utils.response import user_standard_response, page_response, makePageResult
from type.functions import *
from type.user import Product_interface
from model.user import Product

users_router = APIRouter()
user_model = UserModel()
session_model = SessionModel()
user_info_model = UserinfoModel()
operation_model = OperationModel()
captcha_model = CaptchaModel()
app = FastAPI()

dtype_mapping = {
    'username': str,
    'password': str,
    'email': str,
    'card_id': str,
    'realname': str,
    'gender': int,
    'enrollment_dt': datetime.date,
    'graduation_dt': datetime.date
}

# 输入账号密码进行登录
@users_router.post("/login")
@user_standard_response
async def user_login(log_data: login_interface, request: Request, user_agent: str = Header(None)):
    user_information = user_model.get_user_by_usernametype(log_data.username, log_data.type)
    if user_information is None: # 为空说明用户名不存在
        return {'message': '用户名或密码不正确', 'data': False, 'code': 1}
    else:   # 用户名存在
        new_password = log_data.password

        msg_bytes = new_password.encode("utf8")
        salt = "477d15cb740ca1da08f6d851361b3c80"
        salt_bytes = salt.encode("utf8")
        n, r, p = 4, 8, 16
        hmac = scrypt(msg_bytes, salt=salt_bytes, n=n, r=r, p=p)
        HashPassword = hmac.hex()

        if HashPassword == user_information.password:
            token = str(uuid.uuid4().hex)
            session = session_interface(user_id=int(user_information.id), ip=request.client.host,
                                        func_type=0,
                                        token=token, user_agent=user_agent, exp_dt=
                                        get_time_now('days', 14))
            session_model.add_session(session)

            return {'message': '登陆成功', 'data': {"token": token}, 'code': 0}
        else:
            return {'message': '用户名或密码不正确', 'data': False, 'code': 1}

# 进行个人信息修改
@users_router.post("/edit")
@user_standard_response
async def user_edit(log_data: user_edit_interface):
    Address = log_data.address
    Phone = log_data.phone_number
    Id_card = log_data.id_card
    Token = log_data.token

    valid_phone = user_model.get_user_by_phone(log_data.phone_number) # 判断用户修改后的手机号是否被其他用户使用
    if valid_phone is not None: # 不为空说明手机号已经存在
        return {'message': '该手机号已经被使用，请重新输入', 'data': False, 'code': 1}

    valid_id = user_model.get_user_by_id(log_data.id_card) # 判断用户修改后的身份证号是否被其他用户使用
    if valid_id is not None: # 不为空说明身份证号已经存在
        return {'message': '该身份证号已经被使用，请重新输入', 'data': False, 'code': 1}

    user = user_edit_interface()
    user.address = Address
    user.phone_number = Phone
    user.id_card = Id_card
    user.token = Token

    user_model.edit_user(user)

    return {'message': '修改成功', 'data':{"first_time": False}, 'code': 0}
'''
# 下线
@users_router.put("/logout")
@user_standard_response
async def user_logout(request: Request):
    token = session['token']
    mes = session_model.delete_session_by_token(token)  # 将session标记为已失效
    session_db.delete(token)  # 在缓存中删除
    return {'message': '下线成功', 'data': {'result': mes}, 'token': '-1', 'code': 0}
'''


















