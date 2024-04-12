import shutil

from fastapi import UploadFile
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func, join, update, desc
import model.user
from model.db import dbSession, dbSessionread
from model.user import User,Session,Product,Shop
from type.shop  import shop_request,search_shop,shop_updata,add_shop_interface
import datetime


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
    def update_shop(self,obj:shop_updata):
        with self.get_db() as session:
            session.query(Product).filter(Product.id == id).update(obj)
            session.commit()
            return id

    def add_shop(self,obj:add_shop):
        # try:
        #     obj_dict = jsonable_encoder(obj)
        #     shop_add = Shop(**obj_dict)
        #     shop_add.sales_volume = 0
        #     shop_add.creation_time = datetime.datetime.now()
        #     shop_add.name = add_shop.name
        #     shop_add.user_id = add_shop.user_id
        #     with self.get_db() as session:
        #         session.add(shop_add)
        #         session.commit()
        #         return shop_add.id
        # except Exception as e:
        #     # 如果添加失败，回滚会话以取消之前的操作
        #     session.rollback()
        #     # 返回自定义的错误类实例，包含错误信息
        #     raise str(e)

        try:
            obj_dict = jsonable_encoder(obj)
            '''
            shop_add = Shop(**obj_dict)
            shop_add.sales_volume = 0
            shop_add.creation_time = datetime.datetime.now()
            shop_add.name = add_shop.name
            shop_add.user_id = add_shop.user_id'''
            shop_add = Shop(name=obj.name, user_id=obj.user_id, creation_time=datetime.datetime.now(),
                            sales_volume=0, picture = obj.photo ,address=obj.address)
            with self.get_db() as session:
                session.add(shop_add)
                session.commit()
                return shop_add.id
        except Exception as e:
            # 如果添加失败，回滚会话以取消之前的操作
            session.rollback()
            # 返回自定义的错误类实例，包含错误信息
            raise str(e)


    def delete_shop(self, id: int):  # 删除商品
            with self.get_db() as session:
                shop = session.query(Shop).filter(Shop.id == id).first()
                if shop is None:
                    # 如果没有找到商品，则返回None
                    return None
                # 删除商品
                session.delete(shop)
                session.commit()
                return id