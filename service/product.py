import shutil

from fastapi import UploadFile
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func, join, update, desc
import model.user
from model.db import dbSession, dbSessionread
from model.user import User,Session,Product,Order,Shop,Comment
from type.product import product_add_interface,ProductBuy,comment_add
from service.user import UserModel
from type.product import comment_add

usermodel = UserModel()

class ProductModel(dbSession, dbSessionread):

    def add_product(self, obj: product_add_interface):  # 管理员添加一个商品
        try:
            obj_dict = jsonable_encoder(obj)
            product_add = Product(**obj_dict)
            with self.get_db() as session:
                session.add(product_add)
                session.commit()
                return product_add.id
        except Exception as e:
            # 如果添加失败，回滚会话以取消之前的操作
            session.rollback()
            # 返回自定义的错误类实例，包含错误信息
            raise str(e)

    def update_product(self, id: int, update_data: dict):  # 更新商品信息
        with self.get_db() as session:
            product = session.query(Product).filter(Product.id == id).update(update_data)
            session.commit()
            if product == None :
                return None
            else :
                return id

    def delete_product(self, id: int):  # 删除商品
        with self.get_db() as session:
            product = session.query(Product).filter(Product.id == id).first()
            if product is None:
                # 如果没有找到商品，则返回None
                return None
            # 删除商品
            session.delete(product)
            session.commit()
            return id

    def get_product_by_id(self, id: int):  # 根据商品ID查询商品信息
        with self.get_db_read() as session:
            product = session.query(Product).filter(Product.id == id).first()
            return product

    def get_products_by_category(self, category: str):  # 根据商品类别查询商品列表
        with self.get_db_read() as session:
            products = session.query(Product).filter(Product.category == category).all()
            return products

    def get_products_by_price_range(self, min_price: float, max_price: float):  # 根据价格范围查询商品列表
        with self.get_db_read() as session:
            products = session.query(Product).filter(Product.price >= min_price, Product.price <= max_price).all()
            return products

    def get_products_by_name(self, name: str):  # 根据商品名称查询商品列表
        with self.get_db_read() as session:
            products = session.query(Product).filter(Product.name.like(f'%{name}%')).all()
            return products

    def get_total_products_count(self):  # 获取商品总数
        with self.get_db_read() as session:
            total_count = session.query(Product).count()
            return total_count

    def get_products(self, limit: int):  # 获取前几个产品
        with self.get_db_read() as session:
            products = session.query(Product).filter(limit).all()
            return products

    def get_all_products(self):
        with self.get_db_read() as session:
            products = session.query(Product).all()
            return products

    def get_products_shop(self,shop_id : int):
        with self.get_db_read() as session:
            products = session.query(Product).filter(Product.id == shop_id).all()
            return products

    def save_upload_file(self, upload_file: UploadFile, destination: str):
        with open(destination, "wb") as file_object:
            shutil.copyfileobj(upload_file.file, file_object)
    def purchase_product(self, buy_pro : ProductBuy):
        try:
            with self.get_db() as session:
                # 查询商品是否存在
                product = session.query(Product).filter(Product.id == ProductBuy.pro_id).first()
                if product is None:
                    raise ValueError("Product not found")

                # 检查库存是否足够
                if product.stock < ProductBuy.number:
                    raise ValueError("Not enough stock available")

                # 减少库存量
                product.stock -= ProductBuy.number
                temp = self.get_product_by_id(ProductBuy.user_id);
                order = Order(
                    product_id = ProductBuy.pro_id,
                    user_id = buy_pro.user_id,
                    quantity = buy_pro.number,
                    amount = temp.price * buy_pro.number,
                    address =  UserModel.get_user_by_id(ProductBuy.user_id).address,
                    status = 1,  # 假设初始状态为1，表示订单已创建
                    create_dt=func.now()
                )
                # 添加订单到数据库
                session.add(order)
                session.commit()

                return order.id

        except Exception as e:
            # 如果购买失败，回滚会话以取消之前的操作
            session.rollback()
            # 返回错误信息
            raise e


    def add_shop(self, shop_name: str):
        with self.get_db_read() as session:
            NewShop = Shop(name=shop_name, user_id=1)
            session.add(NewShop)
            session.commit()

    def add_comment(self, temp_comment : comment_add):
        tt = usermodel.get_finished_order_by_id(comment_add.user_id,comment_add.product_id)
        if tt == None :
            return None


        else :
            with self.get_db_read() as session:
                cc = Comment(review=comment_add.review,product_id=comment_add.product_id,user_id=comment_add.user_id)
                session.add(cc)
                session.commit()
            return 1
