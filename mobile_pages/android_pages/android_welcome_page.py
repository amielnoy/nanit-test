from infra.mobile_session import MobileSession
from mobile_pages.base_page import BasePage


class AndroidWelcomePage(BasePage):
    def __init__(self, session: MobileSession):
        super().__init__(session, "login_button_android")

    def tap_login(self):
        self.session.click("login_button_android")
