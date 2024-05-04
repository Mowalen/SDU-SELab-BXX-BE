from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, UploadFile, Form, File
from fastapi import Request, Header, Depends
from model.db import session_db, user_information_db
from service.manager import ManagerModel
from controller.user import user_model
from type.functions import get_time_now
from type.manager import product_interface, edit_product_interface
from type.user import login_interface, session_interface, register_interface, user_add_interface, user_edit_interface, \
    order_interface, shop_interface, shop_id_interface
from utils.response import user_standard_response

manager_router = APIRouter()
manager_model = ManagerModel()

# 管理待开业的店铺
@manager_router.post("/shop")
@user_standard_response
async def manager_shop(request: Request):
    headers = request.headers
    Token = headers.get('Authorization')

    shop_list = manager_model.get_all_shop()
    open_shop = []
    close_shop = []
    open_SHOP = []
    close_SHOP = []
    for shop in shop_list:
        if shop.status == 0:
            close_shop.append(shop)
        else:
            open_shop.append(shop)

    for item in open_shop:
        shop = shop_interface()
        shop.shop_name = item.name # 商铺名称
        shop.photo = item.picture # 商铺图片
        shop.address = item.address # 商铺地址
        shop.sales_volume = item.sales_volume # 商铺销售额
        shop.time = str(item.creation_time) # 商铺创建时间

        order_list = user_model.get_order_by_shop_id(item.id) # 获取该商铺中所有订单

        for order in order_list:
            product = order_interface()
            product_infor = user_model.get_product_by_product_id(order.product_id) # 根据商品id获取商品信息
            product.name = product_infor.name  # 商品名字
            product.shop_id = item.id  # 店铺id
            product.photo = product_infor.picture  # 商品照片
            product.address = order.address  # 商品到达地址
            product.quantity = order.quantity  # 商品数量
            product.shop_name = item.name # 商铺名称
            product.amount = order.amount  # 商品价钱
            product.status = order.status  # 商品状态
            product.order_id = order.id  # 该订单的订单号
            product.product_id = order.product_id  # 商品id
            product.time = str(order.create_dt)  # 该订单的创建时间
            shop.order.append(product.model_dump())
        open_SHOP.append(shop.model_dump())

    for item in close_shop:
        shop = shop_interface()
        shop.shop_name = item.name # 商铺名称
        shop.photo = item.picture # 商铺图片
        shop.address = item.address # 商铺地址
        shop.sales_volume = item.sales_volume # 商铺销售额
        shop.time = str(item.creation_time) # 商铺创建时间
        close_SHOP.append(shop.model_dump())
    return {'message': '查看成功', 'data': {"SHOP": open_SHOP, "Shop": close_SHOP}, 'code': 0}

# 允许开业的店铺
@manager_router.post("/edit_shop")
@user_standard_response
async def edit_shop_status(request: Request, log_data: edit_product_interface):
    headers = request.headers
    Token = headers.get('Authorization')
    manager_model.edit_shop(log_data.shop_id)
    return {'message': '修改成功', 'data': False, 'code': 0}

# 查看所有商品
@manager_router.post("/product")
@user_standard_response
async def manager_product(request: Request):
    headers = request.headers
    Token = headers.get('Authorization')

    allow_product = [] # 已上架商品
    unallow_product = [] # 待上架商品

    Item = manager_model.get_all_product()
    for item in Item:
        product = product_interface()
        product.product_id = item.id # 商品id
        product.product_name = item.name # 商品名称
        product.price = item.price # 商品价格
        product.product_category = item.category # 商品分类
        product.product_description = item.description # 商品描述
        product.product_picture = item.picture # 商品图片
        product.product_stock = item.stock # 商品库存
        product.shop_id = item.shop_id #所属商铺id
        shop = manager_model.get_shop_by_id(item.shop_id)
        product.shop_name = shop.name
        product.shop_picture = shop.picture
        product.shop_address = shop.address
        if item.status == 0:
            unallow_product.append(product.model_dump())
        else:
            allow_product.append(product.model_dump())
    return {'message': '修改成功', 'data': {"Product": allow_product, "Products": unallow_product}, 'code': 0}

# 管理待通过的商品
@manager_router.post("/edit_product")
@user_standard_response
async def edit_product_status(request: Request, log_data: edit_product_interface):
    headers = request.headers
    Token = headers.get('Authorization')
    manager_model.edit_product(log_data.product_id)
    return {'message': '修改成功', 'data': False, 'code': 0}