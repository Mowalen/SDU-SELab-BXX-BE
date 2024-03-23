from model.user import Product
from utils.response import product_response
from fastapi import APIRouter, HTTPException,FastAPI
from service.product import ProductModel
from type.product import product_add_interface,ProductResponse,ProductRequest

pro_router = APIRouter()

#返回所有商品

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
    return product_model.add_product(product)

@pro_router.put("/products/{product_id}")
@product_response
def update_product(product_id: int, update_data: dict, product_model: ProductModel ):
    return product_model.update_product(product_id, update_data)

@pro_router.delete("/products/{product_id}")
@product_response
def delete_product(product_id: int, product_model: ProductModel ):
    return product_model.delete_product(product_id)