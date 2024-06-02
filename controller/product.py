import random
from urllib.parse import urljoin

from fastapi.responses import FileResponse
from fastapi import Request, Form

import type.product
from model.user import Product
from type.shop import pro_update
from utils.response import *
from fastapi import APIRouter, HTTPException, FastAPI, UploadFile, File, Query
from service.product import ProductModel
from type.product import product_add_interface, ProductRequest, ProductSearch
from service.user import UserModel, SessionModel
from type.product import *
from service.user import UserModel, SessionModel
from service.shop import ShopModel
from utils.data import *
from type.product import *

products_router = APIRouter()
index_router = APIRouter()
product_model = ProductModel()
session_model = SessionModel()
shopmodel = ShopModel()
user_model = UserModel()


@products_router.get("/detail")
@standard_response
async def get_product(request: Request, product_id: int = Query()):
    Product = product_model.get_product_by_id(product_id)
    if(Product.status == 0):
        return {"code":1}
    elif (Product == None):
        return {"code": 1}
    else:
        base_url = str(request.base_url)
        image_url = urljoin(base_url, "/static/img/Ajax.jpg")
        return {
            "code": 1,
            "image": Product.picture,
            "description": Product.description,
            "price": Product.price,
            "name": Product.name,
            "shop": {
                "id": Product.shop_id,
                "name": shopmodel.get_shop_info(Product.shop_id).name
            }

        }

@products_router.post("/add")
@standard_response
async def add_product(request: Request, product: product_add_interface):
    if product_model.add_product(product) == 'e':
        return {
            "code": 0
        }
    else:
        return {
            "code": 1
        }


@products_router.post("/detail")
@standard_response
async def add_product(request: Request, product: product_add_interface):
    if product_model.add_product(product) == 'e':
        return {
            "code": 0
        }
    else:
        return {
            "code": 1
        }


@products_router.post("/detail/change")
@standard_response
async def update_product(request: Request, product_id: int = Form(None), price: float = Form(None),
                         name: str = Form(None), description: str = Form(None), shop_id: int = Form(None),
                         stock: int = Form(None), image: UploadFile = File(None)):
    update_data = pro_update()
    update_data.product_id = product_id
    update_data.price = price
    update_data.name = name
    update_data.description = description
    update_data.shop_id = shop_id
    update_data.stock = stock
    update_data.image = image
    t = product_model.update_pro(update_data)
    return{"code": 1}

@products_router.post("/detail/del")
@standard_response
async def delete_product(request: Request,tt:  comment_del):
    aa = product_model.delete_product(tt)
    if aa == 1:
        return{"code" : 1}
    else:
        return {"code" : 0}

@index_router.get("/")
@standard_response
async def get_homepage(request: Request):
    headers = request.headers
    Token = headers.get('Authorization')
    User = user_model.get_user_by_token(Token)
    prefrence_list = []

    temp = bin(User.preference).replace('0b','')
    i = len(temp)
    for it in temp:
        i = i - 1
        if it == '1':
            prefrence_list.append(i)
    recommendation_list = []
    cnt = 0
    while cnt < 3:
        t = random.randint(1, 16)
        if t not in recommendation_list:
            cnt += 1
            prefrence_list.append(t)

    for it in prefrence_list:
        recommendations = product_model.get_products(it)
        for item in recommendations:
            recommendation_list.append(item)

    random.shuffle(recommendation_list)
    recommendation =[
        {"id": product.id, "name": product.name, "url": product.picture, "price": str(product.price)}
        for product in recommendation_list
    ]

    big_picture_data = product_model.get_bigpicture_product()
    big_picture = [
        {"id": product.id, "name": product.name, "url": "/static/bigpicture/" + str(product.id) + ".png", "price": str(product.price)}
        for product in big_picture_data
    ]

    return {'big_pictures': big_picture,
            'recommends': recommendation,
            "code": 0
    }

@products_router.post("/search")
@standard_response
async def search_product(search_pro: ProductSearch):
    products = product_model.get_products_by_name(search_pro.search_str)
    if products == None:
        return {
            "code": 1
        }
    else:
        temp = [
            {"product_id": product.id, "productname": product.name, "price":product.price, "url": product.picture}
            for product in products
        ]
        return temp

@products_router.post("/test_img")
@standard_response
async def upload_file(request: Request, file: UploadFile = File(...)):
    db = ProductModel()
    try:
        # 检查文件类型
        if file.content_type.startswith('image'):
            # 保存文件到指定位置
            db.save_upload_file(file, f"uploaded_files/{file.filename}")
            return 1
        else:
            return 2
    except Exception as e:
        return str(e)


@products_router.post("/detail")
@standard_response
async def buy_pro(request: Request, buy_pro: ProductBuy):
    tt = ProductModel.purchase_product(ProductBuy)
    if tt == 'e':
        return {
            "code": 1
        }
    else:
        return {
            "code": 0
        }


@products_router.get("/acquire_img")
async def acquire_image(path: str = Query()):
    # 从文件系统中读取图片内容
    return FileResponse(path, media_type="image/png")


@products_router.post("/add_shop")
@standard_response
async def add_product():
    db = ProductModel()
    lines = xihu.strip().split('\n')

    # 初始化结果列表
    result = []

    # 遍历每一行
    for line in lines:
        # 按空格分割，并添加到结果列表中
        result.append(line.split(' '))

    for i in result:
        db.add_existed_shop(i[2])
    return 'OK'


@products_router.post("/add_product")
@standard_response
async def add_product():
    db = ProductModel()
    lines = xihu.strip().split('\n')

    # 初始化结果列表
    result = []

    # 遍历每一行
    for line in lines:
        # 按空格分割，并添加到结果列表中
        result.append(line.split(' '))

    name_dict = {}

    for i in result:
        shop_id = db.search_shop_id(i[2])
        db.add_existed_product(i[0], i[1], shop_id, 500, i[3], 1)
    return 'OK'


@products_router.put("/update_existed_product")
@standard_response
async def add_product():
    db = ProductModel()
    lines = wenju.strip().split('\n')

    # 初始化结果列表
    result = []
    i = 55
    # 遍历每一行
    for line in lines:
        index = line.find(".jpg")
        description = line[index + len(".jpg"):]
        db.update_existed_product(description, i)
        i += 1
    return 'OK'


@products_router.get("/get_all_products_from_shop")
@standard_response
async def get_all_products_from_shop(request: Request, shop_id: int = Query()):
    db = ProductModel()
    return db.search_all_products(shop_id)


@products_router.post("/shopkeeper_add_product")
@standard_response
async def shopkeeper_add_product(request: Request, description: str = Form(...),
                                 price: float = Form(...),
                                 name: str = Form(...),
                                 shop_id: int = Form(...),
                                 stock: int = Form(...),
                                 image: UploadFile = File(...)):
    db = ProductModel()
    return db.shopkeeper_add_product(description, price, name, shop_id, stock, image)


@products_router.post("/detail/comment")
@user_standard_response
async def comment_add(request: Request,temp_comment: comment_add):
    headers = request.headers
    Token = headers.get('Authorization')
    User = user_model.get_user_by_token(Token)
    temp_comment.user_id = User.id
    aa = product_model.add_comment(temp_comment)
    if aa == 'error':
        return {"message": '尚未购买，无法评论', 'data': False, "code": 1}
    else:
        return {"message": 'success', 'data': False, "code": 0}

@products_router.post("/detail/buy1")
@user_standard_response
async def buy_product1(request: Request, buy_pro: ProductBuy):   # 商品直接购买
    headers = request.headers
    Token = headers.get('Authorization')
    User = user_model.get_user_by_token(Token)
    buy_pro.user_id = User.id
    category = product_model.get_category_of_product(buy_pro.product_id)
    preference = bin(User.preference).replace('0b','').zfill(16)
    modified_preference = product_model.change_preference(preference=preference)
    string_list = list(modified_preference)
    string_list[category-1] = '1'
    new_string = ''.join(string_list)
    new_preference = int(new_string, 2)
    user_model.save_preference(user_id=1, preference=new_preference)
    tt = product_model.purchase_product1(buy_pro)
    if tt == "e":
        return {"message": 'error', "code": 0}
    else:
        if tt == 0:
            return {'message': 'Product not found', 'data': False, 'code': 1}
        if tt == 1:
            return {'message': 'Not enough stock available', 'data': False, 'code': 1}
        if tt == 2:
            return {"message": 'success', "code": 0}

@products_router.post("/detail/buy2")
@standard_response
async def buy_product2(request: Request, buy_pro: ProductBuy):   # 商品添加至购物车
    headers = request.headers
    Token = headers.get('Authorization')
    User = user_model.get_user_by_token(Token)
    category = product_model.get_category_of_product(buy_pro.product_id)
    preference = bin(User.preference).replace('0b','').zfill(16)
    modified_preference = product_model.change_preference(preference=preference)
    string_list = list(modified_preference)
    string_list[category-1] = '1'
    new_string = ''.join(string_list)
    new_preference = int(new_string, 2)
    user_model.save_preference(user_id=1, preference=new_preference)
    buy_pro.user_id = User.id
    tt = product_model.purchase_product2(buy_pro)
    if tt == "e":
        return 'error'
    else:
        return 'success'


@products_router.get("/detail/buy")  # 用户购买页面信息接口
@standard_response
async def getuserbuyinfo(request: Request):
    headers = request.headers
    Token = headers.get('Authorization')
    User = user_model.get_user_by_token(Token)
    return {
        "address": User.address,
        "phone_number": User.phone_number
    }

@products_router.post("/detail/comment/search")
@standard_response
async def search_comment(request: Request, tempsearch: comment_search):
    cc = product_model.search_comment(tempsearch.search_str)
    if cc == None:
        return 'error'
    ttc = [
        {"comment_id": comment.id, "review": comment.review, "user_id": comment.user_id,
         "user_name": user_model.get_username_by_id(comment.user_id)}
        for comment in cc
    ]
    return ttc


@products_router.post("/detail/comment/view")
@standard_response
async def get_comment(request:Request , get_comment: comment_get):
    headers = request.headers
    Token = headers.get('Authorization')
    cc = product_model.get_comment(get_comment.product_id)
    ttc = []
    for comment in cc:
        c = comment_get_all()
        c.comment_id = comment.id
        c.review = comment.review
        c.user_id = comment.user_id
        c.user_name = user_model.get_user_by_token(Token).username
        c.create_time = str(comment.create_dt)
        ttc.append(c.model_dump())
    return ttc

# 0：用户将该商品放入购物车
# 1：表示用户已经付款尚未发货
# 2： 表示商品已经发货但没送达
# 3：商品已经送达未点击确定收货
# 4：商品确定收货


@products_router.post("/detail/refund")
@user_standard_response
async def refund(request: Request, log_data: pro_refund):
    headers = request.headers
    Token = headers.get('Authorization')
    temp_order = product_model.get_status_f_orderid(log_data.order_id)
    if(temp_order.status == 4):
        return {'message': '商品已退款，无法退款','data': False, 'code': 1}
    product_model.refund_deal(temp_order.product_id, temp_order.quantity, temp_order.amount, log_data.order_id)
    return {'message': 'success','data': False, 'code': 0}


@products_router.post("/search/category")
@standard_response
async def search_product_by_category(request: Request, category: category_interface):
    headers = request.headers
    Token = headers.get('Authorization')
    products = product_model.get_products(category=category.category, limit=30)
    temp = [
        {"product_id": product.id, "productname": product.name, "price": product.price, "url": product.picture}
        for product in products
    ]
    return temp

@products_router.post("/sell_out") # 商品下架
@standard_response
async def sell_out(request: Request, log_data: product_interface):
    headers = request.headers
    Token = headers.get('Authorization')
    product_model.sell_out(log_data.product_id)
    return 'success'

@products_router.post("/reapply") # 商品重新提交
@standard_response
async def reapply(request: Request, log_data: product_interface):
    headers = request.headers
    Token = headers.get('Authorization')
    product_model.reapply(log_data.product_id)
    return 'success'


@products_router.post("/dialog")
@standard_response
async def dialog(request: Request, log_data: dialog_add):
    headers = request.headers
    Token = headers.get('Authorization')
    product_model.add_dialog(log_data.send_id, log_data.receive_id, log_data.dialog)
    return 'success'

@products_router.post("/get_dialog")
@standard_response
async def get_dialog(request: Request, send_id: int, receive_id: int):
    headers = request.headers
    Token = headers.get('Authorization')
    result = product_model.get_dialog(send_id, receive_id)
    return result
