from infra.mobile_session import MobileSession


class BasePage:
    def __init__(self, session: MobileSession, element_id: str):
        self.session = session
        self._element_id = element_id

    def is_visible(self) -> bool:
        return self.session.is_visible(self._element_id)

    def wait_until_visible(self, timeout: float = 3.0):
        return self.session.wait_for_visibility(self._element_id, timeout=timeout)
