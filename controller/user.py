import datetime
import json
import random
import string
import uuid
from pydantic import main
from fastapi import APIRouter, HTTPException
from fastapi import Request, Header, Depends
from model.db import session_db, user_information_db
from service.user import UserModel, SessionModel, UserinfoModel, OperationModel, CaptchaModel
from type.user import user_info_interface, \
    session_interface, email_interface, password_interface, user_add_interface, admin_user_add_interface, \
    login_interface, \
    captcha_interface, user_interface, reason_interface, user_add_batch_interface, oj_login_interface
from utils.response import user_standard_response, page_response, makePageResult
from type.functions import *

users_router = APIRouter()
user_model = UserModel()
session_model = SessionModel()
user_info_model = UserinfoModel()
operation_model = OperationModel()
captcha_model = CaptchaModel()
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
    user_information = user_model.get_user_by_username(log_data.username)  # 先查看要登录的用户名是否存在
    if user_information is None:  # 用户名不存在
        return {'message': '用户名或密码不正确', 'data': False, 'code': 1}
    else:  # 用户名存在
        new_password = log_data.password
        if new_password == user_information.password:
            status = user_model.get_user_status_by_username(log_data.username)[0]  # 登陆时检查帐号状态
            if status == 1:
                return {'message': '账号未激活', 'data': {"first_time": True}, 'code': 0}
            elif status == 2:
                return {'message': '账号已注销', 'data': False, 'code': 3}
            elif status == 3:
                return {'message': '账号被封禁', 'data': False, 'code': 4}
            token = str(uuid.uuid4().hex)
            session = session_interface(user_id=int(user_information.id), ip=request.client.host,
                                        func_type=0,
                                        token=token, user_agent=user_agent, exp_dt=
                                        get_time_now('days', 14))
            id = session_model.add_session(session)
            session = session.model_dump()
            user_session = json.dumps(session)
            session_db.set(token, user_session, ex=1209600)  # 缓存有效session
            return {'message': '登陆成功', 'token': token, 'data': {"first_time": False}, 'code': 0}
        else:
            return {'message': '用户名或密码不正确', 'data': False, 'code': 1}


# 下线
@users_router.put("/logout")
@user_standard_response
async def user_logout(request: Request):
    token = session['token']
    mes = session_model.delete_session_by_token(token)  # 将session标记为已失效
    session_db.delete(token)  # 在缓存中删除
    return {'message': '下线成功', 'data': {'result': mes}, 'token': '-1', 'code': 0}


















