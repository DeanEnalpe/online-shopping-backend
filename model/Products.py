class FSEProducts:
    def __init__(self,
                 product_name,
                 product_description,
                 price,
                 features,
                 quantity,
                 product_status):

        self.product_name = product_name
        self.product_description = product_description
        self.price = price
        self.features = features
        self.quantity = quantity
        self.product_status = product_status

    def convert_to_json(self):
        product_dictionary = {
                        "product_name": self.product_name,
                        "product_description": self.product_description,
                        "price": self.price,
                        "features": self.features,
                        "quantity": self.quantity,
                        "product_status": self.product_status,
                        }
        return product_dictionary