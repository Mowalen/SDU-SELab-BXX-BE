from model.user import Product
from utils.response import product_response,user_standard_response,standard_response
from fastapi import APIRouter, HTTPException, FastAPI, UploadFile, File
from service.product import ProductModel
from service.user import UserModel, SessionModel
from type.shop  import shop_request,search_shop,shop_updata
from service.shop import ShopModel
from service.product import ProductModel
import datetime
from fastapi.encoders import jsonable_encoder
from fastapi import Request, Header, Depends,Form

shop_router = APIRouter()
shopmodel= ShopModel()
user_model = UserModel()
product_model = ProductModel()

@shop_router.get("/detail")
@standard_response
async def get_shop(request: Request,request_data:shop_request):
    temp_shop = shopmodel.get_shop_info(shop_request.id)
    if temp_shop == None:
        return {
            "code" : 1
        }
    owner_name = user_model.get_user_by_id(temp_shop.user_id)
    products = product_model.get_products_shop(shop_request.id)
    return{
            "code" : 0,
            "Shopname" : temp_shop.name,
            "owner_id" : temp_shop.user_id,
            "owner_name":owner_name,
            "create_time" : temp_shop.creation_time,
            "sales_volume" : temp_shop.sales_volume,
            "products" : products
    }

@shop_router.post("/search")
@standard_response
async def search_shop(request: Request,request_data:search_shop):
    shops = shopmodel.search_shop(request_data.temp)
    shop_searched = [
        {
            "code": 0,
            "Shopname": shop.name,
            "owner_id": shop.user_id,
            "owner_name": shopmodel.get_shop_info(shop.id),
            "create_time": shop.creation_time,
            "sales_volume": shop.sales_volume,
    }
    for shop in shops
    ]
    return{
        'data' : shop_searched
    }


@shop_router.post("/detail")
@standard_response
async def update_shop(request: Request,up_data : shop_updata):
    headers = up_data.header()
    Token = headers.get("Authorization")
    up_data.user_id = user_model.get_user_by_token(Token)
    temp = shopmodel.update_shop(up_data)
    if(temp == None) :
        return {
            'error'
        }


@shop_router.post("/add")
@standard_response
async def add_shop(request: Request, shop_name: str = Form(None),
                    address: str = Form(None), Photo: UploadFile = File(None)):
    if shopmodel.add_shop(add_shop) == 'e':
        return {
            'message':'商品添加失败'
        }
    else :
        return {
            'message':'商品添加成功'
        }

@shop_router.delete("/detail")
@standard_response
async def delete_product(request: Request,product_id: int ):
    temp = shopmodel.delete_shop(product_id)
    if temp == None:
        return {
            "message" : '此商品不存在',
            "code" : 1
        }
    else :
        return {
            'message':'删除成功',
            "code": 0
        }

