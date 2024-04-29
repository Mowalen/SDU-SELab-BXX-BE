from urllib.parse import urljoin

from fastapi.responses import FileResponse
from fastapi import Request, Form

import type.product
from model.user import Product
from utils.response import product_response, user_standard_response, standard_response
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
    if (Product == None):
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
async def add_product(request: Request,product: product_add_interface):
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
async def add_product(request: Request,product: product_add_interface):
    if product_model.add_product(product) == 'e':
        return {
            "code": 0
        }
    else:
        return {
            "code": 1
        }


@products_router.put("/detail")
@standard_response
def update_product(request: Request,product_id: int, update_data: dict):
    return product_model.update_product(product_id, update_data)


@products_router.delete("/detail")
@standard_response
async def delete_product(request: Request,tt: comment_add):
    aa = product_model.add_comment(tt)
    if aa == None:
        return {
            "code": 1
        }
    else:
        return {
            "code": 0
        }


@index_router.get("/")
@standard_response
async def get_homepage(request: Request):
    big_picture_data = product_model.get_products(1)
    base_url = str(request.base_url)
    image_url = urljoin("", "/static/img/Ajax.jpg")
    big_picture = [
        {"id": product.id, "name": product.name, "url": image_url}
        for product in big_picture_data
    ]

    return {'big_pictures': big_picture,
            'recommends': big_picture,
            "code": 0
            }


@products_router.post("/search")
@standard_response
async def search_product(request: Request,search_pro: ProductSearch):
    products = product_model.get_products_by_name(search_pro.name)
    if products == None:
        return {
            "code": 1
        }
    else:
        temp = [
            {"id": product.id, "name": product.name, "url": product.picture}
            for product in products
        ]
        return {
            "code": 0,
            "data": temp
        }


@products_router.post("/test_img")
@standard_response
async def upload_file(request: Request,file: UploadFile = File(...)):
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
async def but_pro(request: Request,buy_pro: ProductBuy):
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
    lines = text1.strip().split('\n')

    # 初始化结果列表
    result = []

    # 遍历每一行
    for line in lines:
        # 按空格分割，并添加到结果列表中
        result.append(line.split(' '))

    name_dict = {}

    for i in result:
        if i[2] in name_dict:
            continue
        db.add_existed_shop(i[2])
        name_dict[i[2]] = 1
    return 'OK'


@products_router.post("/add_product")
@standard_response
async def add_product():
    db = ProductModel()
    lines = text1.strip().split('\n')

    # 初始化结果列表
    result = []

    # 遍历每一行
    for line in lines:
        # 按空格分割，并添加到结果列表中
        result.append(line.split(' '))

    name_dict = {}

    for i in result:
        shop_id = db.search_shop_id(i[2])
        db.add_existed_product(i[0], i[1], shop_id, 500, i[3], 0)
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
@standard_response
async def comment_add(request: Request,temp_comment : comment_add) :
    aa = product_model.add_comment(comment_add)
    if aa == 'error' :
        return{
            'error'
        }
    else :
        return{
            'success'
        } 

@products_router.post("/detail/buy1")
@standard_response
async def buy_product1(request: Request,buy_pro: ProductBuy):   # 商品直接购买
    tt = ProductModel.purchase_product1(ProductBuy)
    if tt == "e":
        return{
            'error'
        }
    else:
        return{
            'success'
        }

@products_router.post("/detail/buy2")
@standard_response
async def buy_product2(request: Request,buy_pro: ProductBuy):   # 商品添加至购物车
    tt = ProductModel.purchase_product2(ProductBuy)
    if tt == "e":
        return{
            'error'
        }
    else:
        return{
            'success'
        }

@products_router.get("/detail/buy") #用户购买页面信息接口
@standard_response
async def getuserbuyinfo(request: Request):
    headers = request.headers
    Token = headers.get('Authorization')
    User = user_model.get_user_by_token(Token)
    return{
        "address" : User.address,
        "phone_number" : User.phone_number
    }

@products_router.post("/detail/comment/search")
@standard_response
async def search_comment(request: Request,tempsearch:commnet_search):
    cc = product_model.search_commnet(tempsearch.search_str)
    if cc == None:
        return{
            'error'
        }
    else :
        return{
            cc
        }
