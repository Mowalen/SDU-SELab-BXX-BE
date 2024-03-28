import shutil

from fastapi import UploadFile
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func, join, update, desc
import model.user
from model.db import dbSession, dbSessionread
from model.user import User,Session,Product
from type.user import user_info_interface, session_interface, \
    operation_interface, user_add_interface, education_program_interface
from type.product import product_add_interface,ProductRequest


class ShopModel(dbSession, dbSessionread):

