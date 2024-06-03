class User:
    def __init__(self,
                 first_name,
                 last_name,
                 email,
                 login_id,
                 password,
                 confirm_password,
                 contact_number):

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.login_id = login_id
        self.password = password
        self.confirm_password = confirm_password
        self.contact_number = contact_number

    def convert_to_json(self):
        account_dict = {"first_name": self.first_name,
                        "last_name": self.last_name,
                        "email": self.email,
                        "login_id": self.login_id,
                        "password": self.password,
                        "confirm_password": self.confirm_password,
                        "contact_number": self.contact_number
                        }

        return account_dict

