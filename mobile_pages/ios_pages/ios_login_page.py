from infra.mobile_session import MobileSession
from mobile_pages.base_page import BasePage


class IOSLoginPage(BasePage):
    def __init__(self, session: MobileSession):
        super().__init__(session, "email_input_ios")

    def enter_email(self, email: str):
        self.session.type("email_input_ios", email)

    def enter_password(self, password: str):
        self.session.type("password_input_ios", password)

    def accept_terms(self):
        self.session.set_checkbox("terms_and_conditions_check_box_ios", True)

    def tap_login(self):
        self.session.click("login_button_ios")
