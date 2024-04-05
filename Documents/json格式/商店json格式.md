## 商店相关接口

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
            "Shopname" : name,
            "owner_id" : user_id
            "owner_name":owner_name, 
            "create_time" : creation_time,
            "sales_volume" : sales_volume,

            // 商店的集合
}

```


