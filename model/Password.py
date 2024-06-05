class Password:
    def __init__(self,
                 email,
                 login_id,
                 new_password,
                 confirm_password):

        self.email = email
        self.login_id = login_id
        self.new_password = new_password
        self.confirm_password = confirm_password

    def convert_to_json(self):
        new_password_dict = {
                        "email": self.email,
                        "login_id": self.login_id,
                        "new_password": self.new_password,
                        "confirm_password": self.confirm_password
                        }

        return new_password_dict

