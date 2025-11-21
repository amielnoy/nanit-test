from infra.mobile_session import MobileSession
from mobile_pages.base_page import BasePage


class IOSLiveStreamPage(BasePage):
    def __init__(self, session: MobileSession):
        super().__init__(session, "live_stream_container_ios")

    def get_stream_status(self) -> str:
        return self.session.get_text("stream_status_label_ios")
