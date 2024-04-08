from urllib.parse import urljoin

from fastapi.responses import FileResponse
from fastapi import Request

from model.user import Product
from utils.response import product_response, user_standard_response, standard_response
from fastapi import APIRouter, HTTPException, FastAPI, UploadFile, File, Query
from service.product import ProductModel
from type.product import product_add_interface, ProductRequest, ProductSearch
from service.user import UserModel, SessionModel, UserinfoModel, OperationModel, CaptchaModel
from type.product import product_add_interface,ProductRequest,ProductSearch,ProductBuy
from service.user import UserModel, SessionModel
from service.shop import ShopModel

products_router = APIRouter()
index_router = APIRouter()
product_model = ProductModel()
session_model = SessionModel()



@products_router.get("/detail")
@standard_response
async def get_product(request: Request, product_id: int = Query()):
    Product = product_model.get_product_by_id(product_id)
    if (Product == None):
        return {'message': '商品不存在', 'data': False, 'code': 1}
    else:
        base_url = str(request.base_url)
        image_url = urljoin(base_url, "/static/img/Ajax.jpg")
        return {
                "image": Product.picture,
                "description": Product.description,
                "price": Product.price,
                "name" : Product.name,
                "shop" :{
                    "id" : Product.shop_id,
                    "name" : ShopModel.get_shop_info(Product.shop_id).name
                }

        }


@products_router.post("/add")
@standard_response
async def add_product(product: product_add_interface):
    if product_model.add_product(product) == 'e':
        return {
            'message': '商品添加失败'
        }
    else:
        return {
            'message': '商品添加成功'
        }


@products_router.put("/detail")
@standard_response
def update_product(product_id: int, update_data: dict):
    return product_model.update_product(product_id, update_data)


@products_router.delete("/detail")
@standard_response
async def delete_product(product_id: int):
    temp = product_model.delete_product(product_id)
    if temp == None:
        return {
            'message': '此商品不存在'
        }
    else:
        return {
            'message': '删除成功'
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
            'recommends': big_picture
    }


@products_router.post("/search")
@standard_response
async def search_product(search_pro: ProductSearch):
    products = product_model.get_products_by_name(search_pro.name)
    if products == None:
        return {
            'error'
        }
    else:
        temp = [
            {"id": product.id, "name": product.name, "url": product.picture}
            for product in products
        ]
        return {
            temp
        }


@products_router.post("/test_img")
@standard_response
async def upload_file(file: UploadFile = File(...)):
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
async def but_pro(buy_pro : ProductBuy):
    ProductModel.purchase_product(ProductBuy)




@products_router.get("/acquire_img")
async def acquire_image(path: str = Query()):
    # 从文件系统中读取图片内容
    return FileResponse(path, media_type="image/png")


@products_router.post("/add_shop")
@standard_response
async def add_product():
    text = """
    千里江山文创金属书签高档精致定制刻字创意 24.00 品卓好礼数码专营店 https://img.alicdn.com/imgextra/i3/48881133/O1CN01PszKXk1KExUZBpUAp_!!0-saturn_solar.jpg 
定制笔记本办公会议记录本记事本定做LOGO 10.80 微信号13868551138 https://img.alicdn.com/imgextra/i4/370020173/O1CN0143xA7o1D9HCdgxEz5_!!0-saturn_solar.jpg 
新款国潮党员学习笔记本会议记录本高档礼盒套装单位定制可印logo 5.80 datura淼总 https://img.alicdn.com/imgextra/i1/35597193/O1CN01C8tLhn230RgdeLhyq_!!0-saturn_solar.jpg 
记工本31天2024年新版手帐明细账带日期大格子个人工地带备注可定制定做商务 13.20 天天特卖工厂店 https://gw.alicdn.com/imgextra/O1CN01cutVpo2LY1xv1fx1b_!!3937219703-0-C2M.jpg 
按动可擦笔学生用晶蓝色摩易擦热敏宇航员炭黑色碳素笔黑色蓝色水笔小学生专用练字笔速干橡皮 44.70 天天特卖工厂店 https://gw.alicdn.com/imgextra/O1CN01H866Og2LY1x50oL9J_!!3937219703-0-C2M.jpg 
直液式走珠笔速干黑色中性笔水笔中小学生专用圆珠笔签字笔针管笔黑笔红笔蓝笔笔按动高颜值笔直液笔三色 14.85 天天特卖工厂店 https://gw.alicdn.com/imgextra/O1CN01457YHq2LY1xMpFHLj_!!3937219703-0-C2M.jpg 
小线圈本卡通笔记本子可爱迷你便携随身口袋记事本小学生礼物20本装a6a7学生用横线笔记本读书记录大学生超萌 5.85 天天特卖工厂店 https://gw.alicdn.com/imgextra/O1CN01Q5WcTL2LY1xhMJZAv_!!3937219703-0-C2M.jpg 
莫兰迪色系透明PET索引贴防水可书写带尺活页分类书签简约INS彩色小清新创意N次贴马卡龙复古色备忘留言标注 5.70 天天特卖工厂店 https://gw.alicdn.com/imgextra/O1CN017OGNbE2LY1y6G40z6_!!3937219703-0-C2M.jpg 
小麻薯手帐套装手账套装儿童少女可爱礼盒新款和纸胶带整卷手杖贴纸分装随心配全套手账本本子女孩工具大礼包 28.80 诺优办公用品专营店 https://g-search2.alicdn.com/img/bao/uploaded/i4/i3/2204986878543/O1CN015Eak4B2CykUZFArqu_!!0-item_pic.jpg 
晨光资料册大容量加厚A4多规格透明插页抽取式文件夹学生用试卷证书收纳办公合同资料整理多功能文件袋 10.00 晨光官方旗舰店 https://g-search3.alicdn.com/img/bao/uploaded/i4/i4/682114580/O1CN010FtVQU1jhgpnONxuR_!!0-item_pic.jpg 
得力笔记本子大学生用简约创意A5/B5学生练习本四本装可爱记事本学生缝线本加厚车线本子ins风作业本 4.30 得力官方旗舰店 https://g-search2.alicdn.com/img/bao/uploaded/i4/i1/407910984/O1CN01xAzQCb1J8id9yJLMJ_!!0-item_pic.jpg 
得力台笔固定签字笔防丢笔黑色0.5mm柜台财务酒店吧台桌面台式笔笔座带线办公家用创意中性笔粘桌笔6791 27.80 得力官方旗舰店 https://g-search3.alicdn.com/img/bao/uploaded/i4/i2/407910984/O1CN012xlQXt1J8ifNOvOs4_!!0-item_pic.jpg 
得力省力折页板夹高颜值A4文件板夹横版竖版资料夹学生用试卷整理档案夹写字垫板商务办公用品文件夹板册 16.00 得力官方旗舰店 https://g-search2.alicdn.com/img/bao/uploaded/i4/i2/407910984/O1CN01jk3pjg1J8ieAH2r8X_!!0-item_pic.jpg 
得力按动笔中性笔重手感商务签字笔金属质感0.5mm子弹头高颜值水笔黑色笔圆珠笔弹簧头顺滑油墨按压走珠笔A12 19.80 得力官方旗舰店 https://g-search1.alicdn.com/img/bao/uploaded/i4/i1/407910984/O1CN01cEHFPM1J8idofXxLc_!!0-item_pic.jpg 
得力复古羊巴皮软皮面笔记本子可定制皮面本商务会议工作记录记事日记本a5加厚皮大学生学习考研简约文艺精致 19.80 得力官方旗舰店 https://g-search2.alicdn.com/img/bao/uploaded/i4/i4/407910984/O1CN01jz9t731J8idHMXzY5_!!0-item_pic.jpg 
晨光大馥大桂系列高颜值按动中性笔ST桂花香味笔学生大容量速干考试刷题笔碳素黑小分贝静音水笔大富大贵 15.80 晨光官方旗舰店 https://g-search2.alicdn.com/img/bao/uploaded/i4/i1/682114580/O1CN01cTXk0j1jhgs4lIuDw_!!0-item_pic.jpg 
【多支装】得力纽赛直液式中性笔0.5mm全针管考试用签字笔圆珠笔大容量巨能写学生用碳素笔NS767 11.80 得力官方旗舰店 https://g-search3.alicdn.com/img/bao/uploaded/i4/i3/407910984/O1CN010oYLQB1J8ieRjIsLu_!!0-item_pic.jpg 
三年二班X禾物卡皮巴拉抽拉式便利贴高中生错题便签纸初中生专用考研全粘式标记贴记事贴有粘性标签贴小学生 12.80 三年二班文具旗舰店 https://g-search3.alicdn.com/img/bao/uploaded/i4/i2/2687755709/O1CN01htDySc1s2m4fEBTG3_!!0-item_pic.jpg 
三年二班美好愿景不硌手活页本b5笔记本本子高颜值可拆卸线圈本初中生专用错题本a5横线本考研记事学生日记本 8.80 三年二班文具旗舰店 https://g-search3.alicdn.com/img/bao/uploaded/i4/i1/2687755709/O1CN01Fl4oNI1s2m0PQvHWk_!!0-item_pic.jpg 
抽屉式桌面收纳盒办公室书桌整理办公桌文件置物架桌上储物柜 69.60 sivass希维思旗舰店 https://g-search3.alicdn.com/img/bao/uploaded/i4/i3/2455533844/O1CN01XhJ3bC1eGbGyuIVJJ_!!0-item_pic.jpg 
CAMP露营系列B5高颜值不硌手活页本厚笔记本本子A5硬壳线圈本可拆卸活页夹环扣外壳初中高中生专用大容量简约 12.90 小槑同学文具专营店 https://g-search2.alicdn.com/img/bao/uploaded/i4/i3/2207164432931/O1CN016NZL3l1XWRnDdC0ev_!!0-item_pic.jpg 
日本ZEBRA斑马中性笔JJM88努力自勉款花朵sarasa study黑色水笔速干按动黑笔BJF笔芯学生用学霸樱花限定0.5mm 10.00 联新办公专营店 https://gw.alicdn.com/imgextra/O1CN01FViUQL1ogNs7q7NNV_!!743905254-0-picasso.jpg 
得力小学生卷笔刀儿童手摇削笔刀铅笔削笔器正品削笔机手动转笔刀美术女孩男孩刨耐用笔刀专用小神器套装 9.40 得力好久不见专卖店 https://g-search2.alicdn.com/img/bao/uploaded/i4/i1/2862150152/O1CN01fddKcz1Czf3gFL1sd_!!0-item_pic.jpg 
库洛米刷题笔中性笔高颜值ST头按动笔黑笔水笔学生专用碳素黑色速干签字笔好看的笔ins大容量圆珠笔用品 11.00 离草文具旗舰店 https://g-search1.alicdn.com/img/bao/uploaded/i4/i3/3354968453/O1CN01Wk8JY32CJWpYRzcpa_!!0-item_pic.jpg 
三年二班错题胶带粘贴复印整理神器免抄题纠错写字半透明隐形胶带可粘复制学生用改错字手账胶带胶布 9.60 三年二班文具旗舰店 https://g-search3.alicdn.com/img/bao/uploaded/i4/i3/2687755709/O1CN01IOUKB01s2lvO6Q51Q_!!0-item_pic.jpg 
桌面收纳盒抽屉式办公室置物架工位整理电脑书桌上储物柜茶几 19.90 收纳总动员旗舰店 https://g-search2.alicdn.com/img/bao/uploaded/i4/i1/2457942829/O1CN01RttYrL1WljIbFvdIA_!!0-item_pic.jpg 
超大号橡皮擦卡通可爱创意超大块小学生专用巨无霸少屑儿童橡皮砖幼儿园不留痕像皮擦小恐龙学生奖品大橡皮 5.70 天天特卖工厂店 https://gw.alicdn.com/imgextra/O1CN012DpPTk2LY1xIGQLcR_!!3937219703-0-C2M.jpg 
限定蜡笔小新按动中性笔袋装刷题笔可爱碳素笔少女心超顺滑笔0.5mm笔芯st笔头学生速干黑色水性签字笔大学 11.85 天天特卖工厂店 https://gw.alicdn.com/imgextra/O1CN01AH6FxC2LY1x52X4Xo_!!3937219703-0-C2M.jpg 
透明pet便利贴纸可写学生用重点标记书写无遮拦防水贴粘性强做笔记网红ins风创意简约便签纸个性标签纸大号 20.85 天天特卖工厂店 https://gw.alicdn.com/imgextra/O1CN01ZKYijp2LY1xeZKxS3_!!3937219703-0-C2M.jpg 
200支中性笔专用笔学生用0.5/0.38mm碳素黑色水性签字水笔圆珠笔红蓝笔芯心全针管子弹头初中生用品速干 5.85 天天特卖工厂店 https://gw.alicdn.com/imgextra/O1CN01rETEAz2LY1xQQI31O_!!3937219703-0-C2M.jpg 
四层超大容量透明笔袋2023新款铅笔盒高颜值男女孩中小学生日系ins风袋高中生简约网红手账工具包女款 29.25 天天特卖工厂店 https://gw.alicdn.com/imgextra/O1CN01n9ZlPr2LY1y5RwwkL_!!3937219703-0-C2M.jpg 
18支荧光笔标记笔学生用记重点强迫症记号笔彩色粗划重点莹光银光做笔记初中双头夜光绘画 5.80 天天特卖工厂店 https://gw.alicdn.com/imgextra/O1CN01xoGSIe2LY1x8Ngaba_!!3937219703-0-C2M.jpg 
晨光读书笔记本摘抄本阅读记录本小学生卡日积月累专用二年级三四六年级语文初中课外积累好词好句 19.90 晨光官方旗舰店 https://g-search1.alicdn.com/img/bao/uploaded/i4/i2/682114580/O1CN01HJobXD1jhgppSQc96_!!682114580.jpg 
晨光八色圆珠笔 卡通可爱创意高颜值多色按压式彩色多功能笔蓝色黑红学生标记号笔记小学生按动园珠笔 12.80 晨光官方旗舰店 https://g-search1.alicdn.com/img/bao/uploaded/i4/i1/682114580/O1CN01fYCayH1jhgsdRqQTp_!!0-item_pic.jpg 
晨光a4文件袋拉链式学科分类袋透明文件档案袋中小学生试卷资料袋科目分类袋大容量多功能拉边袋 33.90 晨光官方旗舰店 https://g-search3.alicdn.com/img/bao/uploaded/i4/i2/682114580/O1CN01NGxpEc1jhgpo6LgsD_!!0-item_pic.jpg 
晨光笔记本子牛皮纸无线装订本A5capable记事本b5简约加厚练习本小大中学生软面抄软抄本商务办公作业本 15.90 晨光官方旗舰店 https://g-search2.alicdn.com/img/bao/uploaded/i4/i1/682114580/O1CN01ywmUNU1jhgu6PSiXG_!!0-item_pic.jpg 
晨光小笔记本子随身携带a7小号迷你横线便携学生记事口袋型简约线圈随手记单词本作业记录本备忘录方格 10.90 晨光官方旗舰店 https://g-search3.alicdn.com/img/bao/uploaded/i4/i1/682114580/O1CN01oNyEwQ1jhgpkzdEc0_!!0-item_pic.jpg 
KACO书源中性笔学生用彩色中性笔彩色笔做笔记专用彩笔多色手账复古色中性笔手帐做笔记的笔一套高颜值 14.75 联新办公专营店 https://g-search2.alicdn.com/img/bao/uploaded/i4/i3/743905254/O1CN01mVgCUa1ogNqAn982e_!!0-item_pic.jpg 
三年二班X长立点点胶点状双面多功能修正带涂改带式透明双面胶学生用涂改错题粘贴手工贴纸便携手账胶 6.80 三年二班文具旗舰店 https://g-search3.alicdn.com/img/bao/uploaded/i4/i1/2687755709/O1CN01qREXsv1s2m3LtQaoU_!!0-item_pic.jpg 
KACOFIRST初心樱花中性笔低重心旋转爱心笔0.5mm速干黑笔刷题考试创意签字笔少女心高颜值学生礼品笔 10.40 联新办公专营店 https://g-search3.alicdn.com/img/bao/uploaded/i4/i2/743905254/O1CN01nF1feD1ogNrAbFsza_!!0-item_pic.jpg 
    """
    db = ProductModel()
    lines = text.strip().split('\n')

    # 初始化结果列表
    result = []

    # 遍历每一行
    for line in lines:
        # 按空格分割，并添加到结果列表中
        result.append(line.split(' '))

    for i in result:
        db.add_shop(i[2])
    return 'OK'
