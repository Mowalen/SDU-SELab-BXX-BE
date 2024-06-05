import requests
import json

url = "http://23.95.222.103:8080/wordscheck"
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}
data = {
    "content": "他在传播艳情内容"
}

response = requests.post(url, headers=headers, data=json.dumps(data))

print("Status Code:", response.status_code)
print("Response Body:", response.json()["return_str"])