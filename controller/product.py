from type.user import Product_interface
from model.user import Product
from utils.response import product_response
from fastapi import APIRouter, HTTPException,FastAPI

app = FastAPI()
@app.get("/products/",response_model=Product_interface)

def get_all_products():
    return Product
#返回所有商品

@app.get("/products/{product_id}",response_model=Product_interface)
@product_response
def get_id_product(product_id:int):
    if product_id < 0 or product_id >= len(Product):
        return {'message': '商品id出错', 'data': False, 'code': 1}
    return  Product[product_id]

@app.post("/products/add")
@product_response
async def add_product(temp_add : Product_interface):
    temp_add.major_id = len(Product)
    Product.append(temp_add)
    return {'message':'商品添加成功'}

@app.put("/products/{product_id}")
@product_response
async def update_product(pro_id: int, update_pro:Product_interface):
    for temp in Product:
        if temp.id == pro_id:
            temp.name = update_pro.name
            temp.category = update_pro.category
            temp.price = update_pro.price
            temp.shop_id = update_pro.shop_id
            return {'message':'商品信息更新成功'}
    return {'message':'商品信息不存在'}

@app.delete("/products/{product_id}")
@product_response
async def delete_pro(pro_id: int):
    for item in Product:
        if item.id == pro_id :
            Product.remove(item)
            return {'message': '商品已删除'}
    return {'message':'商品不存在'}

@app.get("/products/search")
@product_response
async def search_pro(name: str):
    for item in Product:
