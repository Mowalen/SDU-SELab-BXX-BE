from fastapi.testclient import TestClient
from datetime import datetime
from utils.times import getMsTime
from main import app

client = TestClient(app)

def main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "code": 0,
        "message": "OK",
        "data": {"message": "Hello World"},
        #"timestamp": getMsTime(datetime.now())
    }


main()
