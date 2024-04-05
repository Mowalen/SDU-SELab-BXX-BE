from model.user import Product
from utils.response import product_response,user_standard_response,standard_response
from fastapi import APIRouter, HTTPException, FastAPI, UploadFile, File
from service.product import ProductModel
from service.user import UserModel, SessionModel
from type.shop  import shop_request,search_shop
from service.shop import ShopModel

shop_router = APIRouter()
shopmodel= ShopModel()
user_model = UserModel()

@shop_router.post("/detail")
@standard_response
async def get_product(request_data:shop_request):
    temp_shop = shopmodel.get_shop_info(shop_request.id)
    owner_name = user_model.get_user_by_id(temp_shop.user_id)
    return{
            "Shopname" : temp_shop.name,
            "owner_id" : temp_shop.user_id,
            "owner_name":owner_name,
            "create_time" : temp_shop.creation_time,
            "sales_volume" : temp_shop.sales_volume,
    }

@shop_router.post("/search")
@standard_response
async def search_shop(request_data:search_shop):
    shops = shopmodel.search_shop(request_data.str)
    shop_searched = [
        {
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





