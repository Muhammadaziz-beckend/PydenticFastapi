from fastapi import FastAPI

from models import *

app = FastAPI()


@app.post("/users/")
def create_user(user:User):
    return {"message": "Пользователь создан!", "user": user}

@app.post("/product/")
def create_product(product:Product):
    return {"message": "Продукт создан!", "product": product}

@app.post("/car/")
def create_product(car:Car):
    return {"message": "Car создан!", "Car": car}


@app.post("/order/")
def create_product(order:Order):
    return {"message": "Car создан!", "Order": order}
