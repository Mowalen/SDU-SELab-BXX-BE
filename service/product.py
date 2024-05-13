import shutil
from urllib.parse import urljoin

from fastapi import UploadFile
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func, join, update, desc
import model.user
import type.product
import random
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

    def delete_product(self, tt:comment_del):  # 删除商品
        with self.get_db() as session:
            product = session.query(Product).filter(Product.id == tt.comment_id).first()
            if product:
                product.status = 0
                session.commit()
                return 1
            else:
                return 0

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

    def get_products(self, category: int):  # 获取前几个产品
        limit = 10
        Products = []
        with self.get_db_read() as session:
            products = session.query(Product).filter(Product.category == category).all()
            random.shuffle(products)
            for product in products:
                Products.append(product)
                limit = limit - 1
                if limit == 0:
                    break
            return Products

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
            query = session.query(Shop).filter(Shop.name==shop_name).first()
            if query is None:
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

        tt = usermodel.get_finished_order_by_id(temp_comment.user_id, temp_comment.product_id)
        if tt == None:
            return {
                'error'
            }
        else:
            obj_dict = jsonable_encoder(temp_comment)
            cc = Comment(review=temp_comment.review, product_id=temp_comment.product_id, user_id=temp_comment.user_id)
            with self.get_db_read() as session:
                    session.add(cc)
                    session.commit()
            return cc.product_id

    def up_comment(self,temp_comment: comment_update):
        tt = usermodel.get_finished_order_by_id(temp_comment.user_id, temp_comment.product_id)
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
        dbSession.commit()
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
    def search_comment(self,temp:str):
        with self.get_db_read() as session:
            cc = session.query(Comment).filter(Comment.review.like(f'%{temp}%')).all()
            return cc

    def get_comment(self,id : int):
        with self.get_db_read() as session:
            cc = session.query(Comment).filter(Comment.product_id == id).all()
            return cc
    # def update_pro(self,temp : pro_update):
        # with self.get_db_read() as session:
        #     product = session.query(Product).filter(Product.id == temp.product_id).first()
        #
        #     # 如果找到了产品
        #     if product:
        #         # 更新产品的非空属性
        #         if temp.name is not None:
        #             product.name = temp.name
        #         if temp.description is not None:
        #             product.description = temp.description
        #         if temp.price is not None:
        #             product.price = temp.price
        #         if temp.category is not None:
        #             product.category = temp.category
        #         if temp.shop_id is not None:
        #             product.shop_id = temp.shop_id
        #         if temp.stock is not None:
        #             product.stock = temp.stock
        #         if temp.image is not None:
        #             product.image = temp.image
        #
        #         # 提交修改
        #         session.commit()
    def update_pro(self, temp: pro_update):
            with self.get_db_read() as session:
                try:
                    product = session.query(Product).filter(Product.id == temp.product_id).first()

                    # 如果找到了产品
                    if product:
                        # 更新产品的非空属性
                        if temp.name is not None:
                            product.name = temp.name
                        if temp.description is not None:
                            product.description = temp.description
                        if temp.price is not None:
                            product.price = temp.price
                        if temp.category is not None:
                            product.category = temp.category
                        if temp.shop_id is not None:
                            product.shop_id = temp.shop_id
                        if temp.stock is not None:
                            product.stock = temp.stock
                        if temp.image is not None:
                            product.image = temp.image

                        # 提交修改
                        session.commit()
                except Exception as e:
                    # 处理异常
                    session.rollback()  # 回滚事务
                    print("更新产品时发生异常:", e)
                finally:
                    session.close()  # 关闭会话，释放资源

    def get_bigpicture_product(self):
        with self.get_db_read() as session:
            products = session.query(Product).limit(5).all()
            return products


    def get_status_f_orderid(self,temp:pro_refund):
        with self.get_db_read() as session:
            order = session.query(Order).filter(Order.id == temp.order_id).first()
            return order

    def refund_deal(self,product_id : int ,num : int , salesum : int ):
        with self.get_db_read() as session:
            Pro = session.query(Product).filter(Product.id == product_id).first()
            Pro.stock += num
            session.commit()
        with self.get_db_read() as session:
            shop = session.query(Shop).filter(Shop.product_id == product_id).first()
            shop += salesum
            session.commit()





