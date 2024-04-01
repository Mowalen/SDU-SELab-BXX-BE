import shutil

from fastapi import UploadFile
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func, join, update, desc
import model.user
from model.db import dbSession, dbSessionread
from model.user import User,Session,Product,Shop
from type.user import user_info_interface, session_interface, \
    operation_interface, user_add_interface, education_program_interface
from type.product import product_add_interface,ProductRequest


class ShopModel(dbSession, dbSessionread):
    def search_shop(self, keyword):
        """
        根据关键字搜索店铺
        """
        with self.get_db_read() as session:
            shops = session.query(Shop).filter(Shop.name.like(f'%{keyword}%')).all()
            return shops

    def get_shop_info(self, shop_id):
        """
        获取店铺信息
        """
        with self.get_db_read() as session:
            shop = session.query(Shop).filter(Shop.id == shop_id).first()
            return shop


