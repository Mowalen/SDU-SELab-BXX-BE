from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int

user = User(name="John", age=25)

# 使用model_dump()方法返回一个字典
dumped_data = user.model_dump()

print(dumped_data)
# 输出：{'name': 'John', 'age': 25}

# 使用.dict()方法返回一个字典，包含准确的类型信息
dict_data = user.dict()

print(dict_data)
# 输出：{'name': 'John', 'age': 25}

# 打印每个字段的类型
for field_name, field_value in dict_data.items():
    field_type = user.__annotations__[field_name]
    print(f"{field_name}: {field_type}")

# 输出：
# name: <class 'str'>
# age: <class 'int'>