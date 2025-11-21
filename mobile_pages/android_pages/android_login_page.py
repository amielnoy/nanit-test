from infra.mobile_session import MobileSession
from mobile_pages.base_page import BasePage


class AndroidLoginPage(BasePage):
    def __init__(self, session: MobileSession):
        super().__init__(session, "email_input_android")

    def enter_email(self, email: str):
        self.session.type("email_input_android", email)

    def enter_password(self, password: str):
        self.session.type("password_input_android", password)

    def accept_terms(self):
        self.session.set_checkbox("terms_and_conditions_check_box_android", True)

    def tap_login(self):
        self.session.click("login_button_android")
