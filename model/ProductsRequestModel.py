from pydantic import BaseModel


class ProductsRequestModel(BaseModel):
    product_name: str
    product_description: str
    price: str
    features: str
    quantity: str
    product_status: str