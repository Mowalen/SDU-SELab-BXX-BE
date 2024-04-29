import shutil
from operator import and_

from fastapi import UploadFile
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func, join, update, desc
import model.user
from model.db import dbSession, dbSessionread
from model.user import User, Session, Order, Product, Shop
from type.user import session_interface, user_add_interface, user_edit_interface


class UserModel(dbSession, dbSessionread):

    def get_user_by_usernametype(self, username, type):   # 根据username和type查询user的基本信息
        with self.get_db_read() as session:
            user = session.query(User).filter(User.has_delete == 0, User.username == username, User.identity_type == type).first()
            session.commit()
            return user

    def get_finished_order_by_id(self, uid, pid):
            with self.get_db() as session:
                ID = session.query(Order).filter(and_(Order.user_id == uid, Order.product_id == pid, Order.status == 4)).all()
                session.commit()
                return ID

    def get_user_by_username(self, username):   # 只根据username进行查询
        with self.get_db_read() as session:
            user = session.query(User).filter(User.username == username, User.has_delete == 0).first()
            session.commit()
            return user

    def add_user(self, obj: user_add_interface):  # 管理员添加一个用户(在user表中添加一个用户)
        obj_dict = jsonable_encoder(obj)
        obj_add = User(id= obj_dict.get('id'), username=obj_dict.get('username'), password=obj_dict.get('password'),
                       identity_type=obj_dict.get('type'),
                       has_delete=obj_dict.get('has_delete'))
        with self.get_db() as session:
            session.add(obj_add)
            session.commit()
            return obj_add.id

    def get_user_by_token(self, token): # 根据token查用户
        with self.get_db_read() as session:
            ID = session.query(Session).filter(Session.token == token).first()
            session.commit()

        with self.get_db() as session:
            Information = session.query(User).filter(User.id == ID.user_id).first()
            session.commit()
            return Information

    def edit_user(self, obj: user_edit_interface): # 用户修改个人信息
        Address = obj.address
        Phone = obj.phone
        Card = obj.id_card_number
        Photo = obj.photo
        with self.get_db() as session:
            ID = session.query(Session).filter(Session.token == obj.token).first()
            session.commit()

        with self.get_db() as session:
            if Address != None:
                session.query(User).filter(ID.user_id == User.id).update({"address": Address})
                session.commit()
            if Phone != None:
                session.query(User).filter(ID.user_id == User.id).update({"phone_number": Phone})
                session.commit()
            if Card != None:
                session.query(User).filter(ID.user_id == User.id).update({"id_card_number": Card})
                session.commit()
            if Photo != None:
                session.query(User).filter(ID.user_id == User.id).update({"photo": Photo})
                session.commit()

    def edit_order(self, user_id, order_id): # 根据用户id和订单号更改订单状态
        User_id = user_id
        Order_id = order_id
        with self.get_db() as session:
            session.query(Order).filter(Order.id == Order_id, Order.user_id == User_id).update({"status": 4})
            session.commit()

    def get_user_by_phone(self, phone_number, Token):  # 获取用户的手机号，防止重复被使用
        with self.get_db() as session:
            ID = session.query(Session).filter(Session.token == Token).first()
            session.commit()

        with self.get_db_read() as session:
            phone = session.query(User).filter(User.phone_number == phone_number, User.id != ID.user_id).first()
            session.commit()
            return phone

    def get_user_by_id(self, id_card, Token): # 获取用户的身份证号，防止重复被使用
        with self.get_db() as session:
            ID = session.query(Session).filter(Session.token == Token).first()
            session.commit()

        with self.get_db_read() as session:
            id = session.query(User).filter(User.id_card_number == id_card, User.id != ID.user_id).first()
            session.commit()
            return id

    def get_user_by_id(self, id_card): # 获取用户的身份证号，防止重复被使用
        with self.get_db_read() as session:
            id = session.query(User).filter(User.id_card_number == id_card, User.id != ID.user_id).first()
            session.commit()
            return id

    def get_order_by_id(self, id): # 根据用户查询订单
        with self.get_db() as session:
            ID = session.query(Order).filter(Order.user_id == id).all()
            session.commit()
            return ID

    def get_product_by_product_id(self, product_id):
        with self.get_db() as session:
            ID = session.query(Product).filter(Product.id == product_id).first()
            session.commit()
            return ID

    def get_product_shop(self, id): # 根据订单的商品id查商店id
        with self.get_db() as session:
            product = session.query(Product).filter(Product.id == id).first()
            session.commit()
            return product

    def get_order_by_shop_id(self, shop_id): # 根据商家所有商品获取他的所有订单
        with self.get_db() as session:
            product = session.query(Product.id).filter(Product.shop_id == shop_id).all()
            session.commit()

        product_id_list = [product_id[0] for product_id in product]
        with self.get_db() as session:
            product = session.query(Order).filter(Order.product_id.in_(product_id_list)).all()
            session.commit()
            return product

    def get_shop_name(self, id): # 根据商店id查商店name
        with self.get_db() as session:
            shop = session.query(Shop).filter(Shop.id == id).first()
            session.commit()
            return shop

    def get_shop_by_id(self, id): # 根据用户id查询他旗下店铺
        with self.get_db() as session:
            shop = session.query(Shop).filter(Shop.user_id == id).all()
            session.commit()
            return shop

    def get_count(self):    # 查询当前数据库中有多少行，用来记入
        with self.get_db() as session:
            count = session.query(User).count()
            session.commit()
            return count

    def save_upload_file(self, upload_file: UploadFile, destination: str): # 用户上传自己头像（商家也通过该函数上传店铺图片）
        #print(destination)
        with open(destination, "wb") as file_object:
            shutil.copyfileobj(upload_file.file, file_object)

    def add_shop(self, shop): #商家添加店铺
        obj_dict = jsonable_encoder(shop)
        obj_add = Shop(name = obj_dict.get('name'), user_id = obj_dict.get('user_id'),
                       sales_volume = 0,
                      picture = obj_dict.get('photo'),
                       address = obj_dict.get('address'))
        with self.get_db() as session:
            session.add(obj_add)
            session.commit()
            return obj_add.name

class SessionModel(dbSession, dbSessionread):

    def add_session(self, obj: session_interface):  # 添加一个session
        obj_dict = jsonable_encoder(obj)
        obj_dict['exp_dt'] = func.from_unixtime(obj_dict['exp_dt'])
        obj_add = Session(**obj_dict)
        with self.get_db() as session:
            session.add(obj_add)
            session.commit()
            return obj_add.id

    def delete_session_by_token(self, token: str):  # 根据token删除一个session
        with self.get_db() as session:
            session.query(Session).filter(Session.token == token).update({"has_delete": 1})
            session.commit()
            return 'ok'

    def delete_session(self, id: int):  # 根据id删除一个session
        with self.get_db() as session:
            session.query(Session).filter(Session.id == id).update({"has_delete": 1})
            session.commit()
            return id