from model.user import Product
from utils.response import product_response,user_standard_response,standard_response
from fastapi import APIRouter, HTTPException,FastAPI
from service.product import ProductModel
from type.product import product_add_interface,ProductRequest,ProductSearch
from service.user import UserModel, SessionModel, UserinfoModel, OperationModel, CaptchaModel

pro_router = APIRouter()
index_router = APIRouter()
product_model = ProductModel()
session_model = SessionModel()
user_info_model = UserinfoModel()
operation_model = OperationModel()
captcha_model = CaptchaModel()



@pro_router.post("/detail")
@standard_response
async def get_product(request_data: ProductRequest):
    Product = product_model.get_product_by_id(request_data.id)
    if(Product == None):
        return {'message': '商品不存在', 'data': False, 'code': 1}
    else :
        return {
                "image": Product.picture,
                "description": Product.description,
                "price": Product.price
        }



@pro_router.post("/add")
@standard_response
async def add_product(product: product_add_interface):
    if product_model.add_product(product) == 'e':
        return {
            'message':'商品添加失败'
        }
    else :
        return {
            'message':'商品添加成功'
        }

@pro_router.put("/detail")
@standard_response
def update_product(product_id: int, update_data: dict):
    return product_model.update_product(product_id, update_data)

@pro_router.delete("/detail")
@standard_response
async def delete_product(product_id: int ):
    temp = product_model.delete_product(product_id)
    if temp == None:
        return {
            'message':'此商品不存在'
        }
    else :
        return {
            'message':'删除成功'
        }


@index_router.get("/")
@standard_response
async def get_homepage():

    big_picture_data = product_model.get_products(1)
    big_picture = [
        {"id": product.id, "name": product.name, "url": product.picture}
        for product in big_picture_data
    ]

    return {
        'message':'首页信息',
        'data': {
            'bigpicture': big_picture,
            'recommend' : big_picture
        }

    }
@pro_router.post("/search")
@standard_response
async def search_product(search_pro:ProductSearch):
    products = product_model.get_products_by_name(search_pro.name)
    if products == None:
        return {
            'error'
        }
    else :
        temp = [
            {"id": product.id, "name": product.name, "url": product.picture}
            for product in products
        ]
        return{
            temp
        }



