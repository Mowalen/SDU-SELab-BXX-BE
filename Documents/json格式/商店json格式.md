## 商店json格式

### 详情页
#### 请求
```
{
    "shop_id" : id <br>
}
```
#### 返回
```
{
            "Shopname" : name,<br> 
            "owner_id" : user_id,<br> 
            "owner_name":owner_name,<br> 
            "create_time" : creation_time,<br> 
            "sales_volume" : sales_volume,<br> 
} 
```

### 搜索页

#### 请求
```
{
    "search_str" : str<br>
}
```

#### 返回
```
{
            "Shopname" : name,<br> 
            "owner_id" : user_id,<br> 
            "owner_name":owner_name,<br> 
            "create_time" : creation_time,<br> 
            "sales_volume" : sales_volume,<br> 

            // 商店的集合
}

```


