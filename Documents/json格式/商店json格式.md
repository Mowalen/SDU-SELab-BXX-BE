## 商店json格式

### 详情页
#### 请求
{<br>
    "shop_id" : id <br>
}<br>
#### 返回
{<br> 
            "Shopname" : name,<br> 
            "owner_id" : user_id,<br> 
            "owner_name":owner_name,<br> 
            "create_time" : creation_time,<br> 
            "sales_volume" : sales_volume,<br> 
}<br> 
### 搜索页

#### 请求
{<br>
    "search_str" : str<br>
}<br>

#### 返回
{<br> 
            "Shopname" : name,<br> 
            "owner_id" : user_id,<br> 
            "owner_name":owner_name,<br> 
            "create_time" : creation_time,<br> 
            "sales_volume" : sales_volume,<br> 

            // 商店的集合
}<br> 


