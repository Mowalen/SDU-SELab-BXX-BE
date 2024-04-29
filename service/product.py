import shutil
from urllib.parse import urljoin

from fastapi import UploadFile
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func, join, update, desc
import model.user
import type.product
from model.db import dbSession, dbSessionread
from model.user import User, Session, Product, Order, Shop, Comment
from type.product import *
from service.user import UserModel

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
            session.query(Product).filter(Product.id == id).update(update_data)
            session.commit()
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
    def get_comment_by_id(self,int):
        with self.get_db_read() as session:
            comment = session.query(Comment).filter(Comment.id == id).first()
            return comment

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
    def get_coment_of_user(self,user_id : int,comment_id : int):
        with self.get_db_read() as session:
            cc = session.query(Comment).query(Product).filter(comment_id == Comment.id ,user_id == Comment.user_id).first()

            return cc

    def get_products(self, limit: int):  # 获取前几个产品
        with self.get_db_read() as session:
            products = session.query(Product).limit(limit).all()
            return products

    def save_upload_file(self, upload_file: UploadFile, destination: str):
        with open(destination, "wb") as file_object:
            shutil.copyfileobj(upload_file.file, file_object)

    def purchase_product1(self, buy_pro: ProductBuy):
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
                    product_id=ProductBuy.pro_id,
                    user_id=buy_pro.user_id,
                    quantity=buy_pro.number,
                    amount=temp.price * buy_pro.number,
                    address=UserModel.get_user_by_id(ProductBuy.user_id).address,
                    status=1,  # 假设初始状态为1，表示订单已创建
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
    def purchase_product2(self, buy_pro: ProductBuy):
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
                    product_id=ProductBuy.pro_id,
                    user_id=buy_pro.user_id,
                    quantity=buy_pro.number,
                    amount=temp.price * buy_pro.number,
                    address=UserModel.get_user_by_id(ProductBuy.user_id).address,
                    status=0,  # 假设初始状态为1，表示订单已创建
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

    def add_existed_shop(self, shop_name: str):
        with self.get_db_read() as session:
            NewShop = Shop(name=shop_name, user_id=1, status=0)
            session.add(NewShop)
            session.commit()

    def search_shop_id(self, shop_name: str):
        with self.get_db_read() as session:
            shop = session.query(Shop).filter(Shop.name == shop_name).first()
            if shop is not None:
                return shop.id

    def add_existed_product(self, product_name: str, price: float, shop_id: int, stock: int, picture: str, status: int):
        with self.get_db_read() as session:
            NewProduct = Product(name=product_name, price=price, shop_id=shop_id, stock=stock, picture=picture,
                                 status=status)
            session.add(NewProduct)
            session.commit()

    def add_comment(self, temp_comment: comment_add):
        tt = usermodel.get_finished_order_by_id(comment_add.user_id, comment_add.product_id)
        if tt == None:
            return {
                'error'
            }
        else:
            with self.get_db_read() as session:
                cc = Comment(review=comment_add.review, product_id=comment_add.product_id, user_id=comment_add.user_id)
                session.add(cc)
                session.commit()
            return {
                'success'
            }

    def up_comment(self,temp_comment: comment_update):
        tt = usermodel.get_finished_order_by_id(comment_add.user_id, comment_add.product_id)
        if tt == None:
            return {
                'error'
            }
        cc_up = self.get_comment_by_id(temp_comment.id)
        if cc_up == None:
            return{
                'error'
            }
        cc_up.review = temp_comment.update_review
        dbSession.commnit()
        return{
            'success'
        }
    def del_comment(self,temp_comment: comment_del):
        cc = self.get_coment_of_user(comment_del.user_id,comment_del.comment_id)
        if cc == None:
            return{
                'error'
            }
        with self.get_db_read() as session:
            session.delete(cc)
            session.commit()
            return{
                'success'
            }



    def search_all_products(self, shop_id: int):
        with self.get_db_read() as session:
            query = session.query(Product).filter(
                Product.shop_id == shop_id
            ).all()
            ans = []
            for item in query:
                order = session.query(Order).filter(
                    Order.product_id == item.id
                ).count()
                product = {
                    "id": item.id,
                    "name": item.name,
                    "price": item.price,
                    "remaining_quantity": item.stock,
                    "description": item.description,
                    "image": item.picture,
                    "about_orders": order
                }
                ans.append(product)
            return ans

    def shopkeeper_add_product(self, description: str, price: float, name: str, shop_id: int, stock: int, image):
        with self.get_db_read() as session:
            try:
                # 检查文件类型
                if image.content_type.startswith('image'):
                    # 保存文件到指定位置
                    self.save_upload_file(image, f"static/img/{image.filename}")
                    image_url = urljoin("", f"static/img/{image.filename}")
                else:
                    return "Not image"
            except Exception as e:
                return str(e)
            new_product = Product(name=name, price=price, shop_id=shop_id, stock=stock, description=description,
                                  picture=image_url, status=1)
            session.add(new_product)
            session.commit()
            return "OK"
    def search_commnet(self,temp:str):
        with self.get_db_read() as session:
            cc = session.query(Comment).filter(Comment.review.like(f'%{temp}%')).all()
            return cc