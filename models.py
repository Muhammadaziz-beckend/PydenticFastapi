from datetime import datetime,timezone
import re
from typing import List
from pydantic import (
    BaseModel,
    Field,
    validator,
    model_validator,
    field_validator,
)
from typing import ClassVar  # Изменение здесь

class User(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    email: str
    password: str = Field(..., min_length=8)
    confirm_password: str

    @validator("username")
    def validate_username(cls, value: str):
        if " " in value:
            raise ValueError("В имени пользователя не должно быть пробелов!")
        return value.lower()

    @validator("password")
    def validate_password(cls, value: str):
        if not any(char.isdigit() for char in value) and value.isalpha():
            raise ValueError("Пароль должен содержать хотя бы одну цифру!")
        return value

    @validator("email")
    def validate_email(cls, value: str):
        if "@" in value and "." in value:
            return value
        raise ValueError("Email не валиден!")

    @model_validator(mode="after")
    def validate_password_conf(cls, values):
        if values.password != values.confirm_password:
            raise ValueError("Пароли не совпадают")
        return values


class Product(BaseModel):
    # Используем ClassVar для категорий
    __categories: ClassVar[list[str]] = ["electronics", "clothing", "books"]

    name: str
    price: float = Field(..., gt=0)
    category: str
    discount: int = Field(..., gt=0, lt=90)
    description: str = Field(..., max_length=200)

    @validator("name")
    def strip_name(cls, value: str):
        return value.strip()

    @field_validator("category")
    @classmethod
    def validate_category(cls, value):
        if value not in cls.__categories:
            raise ValueError(f"Выберите только из {cls.__categories}")
        return value

    @model_validator(mode="after")
    def validate_discount(cls, values):
        category = values.category
        discount = values.discount
        price = values.price

        if price > 10000 and discount > 0:
            raise ValueError("Запрещена скидка на товары дороже 10 000")

        if category == "electronics" and discount > 30:
            raise ValueError(
                "При категории 'electronics' скидка не должна превышать 30%"
            )
        return values


class Car(BaseModel):
    first_letter: str = Field(..., max_length=1, min_length=1)
    last_letter: str = Field(..., max_length=2, min_length=2)
    city_num: int
    plate_number: str
    year: int
    mileage: int = Field(..., gt=0)

    @validator("plate_number")
    def validate_plate_number(cls, value):
        pattern = r"^[А-Я]{1}\d{3}[А-Я]{2}\d{2}$"
        if not re.match(pattern, value):
            raise ValueError("Номер должен быть в формате 'А123ВС77'")
        return value

    @validator("year")
    def validate_year(cls, value):
        current_year = datetime.now().year
        if current_year - value > 30:
            raise ValueError("Возраст машины не должен превышать 30 лет")
        return value


from typing import ClassVar


class Order(BaseModel):
    STATUS_CHOICES: ClassVar[List[str]] = ["pending", "paid", "shipped"]

    items: List[float]  # Список цен товаров
    total_price: float
    status: str
    created_at: datetime

    @validator("created_at")
    def validate_created_at(cls, value):
        if value > datetime.now(timezone.utc):
            raise ValueError("Дата создания не может быть в будущем")
        return value

    @model_validator(mode="after")
    def validate_total_price(cls, values):
        total = sum(values.items)
        if values.total_price != total:
            raise ValueError("Общая сумма заказа не совпадает с суммой товаров")
        return values

    @validator("status")
    def validate_status(cls, value):
        if value not in cls.STATUS_CHOICES:
            raise ValueError(f"Статус может быть только {cls.STATUS_CHOICES}")
        return value
