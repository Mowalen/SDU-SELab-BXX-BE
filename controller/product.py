from model.user import Product
from utils.response import product_response
from fastapi import APIRouter, HTTPException,FastAPI
from service.product import ProductModel
from type.product import product_add_interface,ProductRequest

pro_router = APIRouter()



@pro_router.get("/products/{product_id}")
@product_response
def get_product(request_data: ProductRequest, product_model: ProductModel ):
    Product = ProductModel.get_product_by_id(ProductRequest.id)
    if(Product == None):
        return {'message': '商品不存在', 'data': False, 'code': 1}
    else :
        return {
            'message':'找到商品',
            "data": {
                "image": Product.image,
                "description": Product.description,
                "price": Product.price
            },
            'code': 0
        }



@pro_router.post("/products/add")
@product_response
def add_product(product: product_add_interface, product_model: ProductModel ):
    if product_model.add_product(product) == 'e':
        return {
            'message':'商品添加失败'
        }
    else :
        return {
            'message':'商品添加成功'
        }

@pro_router.put("/products/{product_id}")
@product_response
def update_product(product_id: int, update_data: dict, product_model: ProductModel ):
    return product_model.update_product(product_id, update_data)

@pro_router.delete("/products/{product_id}")
@product_response
def delete_product(product_id: int, product_model: ProductModel ):
    temp = product_model.delete_product(product_id)
    if temp == None:
        return {
            'message':'此商品不存在'
        }
    else :
        return {
            'message':'删除成功'
        }


@pro_router.post("/homepage")
@product_response
async def get_homepage():

    big_picture_data = ProductModel.get_products(5)
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

