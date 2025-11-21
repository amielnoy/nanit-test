import time
from dataclasses import dataclass, field
from typing import Dict, Optional, Any

from infra.base_session import BaseSession
from infra.streaming_validator import StreamingValidator

SUPPORTED_PLATFORMS = {"ios", "android"}


@dataclass
class MobileSession(BaseSession):
    """
    A lightweight mock of a mobile driver session.

    Simulates navigation and element interactions without real devices.
    """
    platform: str
    api_streaming_validator: StreamingValidator
    env: str = "local"
    metadata: Dict[str, Any] = field(default_factory=dict)

    # runtime state (not part of __init__ signature)
    app_launched: bool = field(default=False, init=False)
    current_screen: str = field(default="welcome", init=False)  # welcome -> login -> live_stream
    state: Dict[str, Optional[str]] = field(default_factory=dict, init=False)

    def __post_init__(self):
        # Initialize the BaseSession part
        BaseSession.__init__(
            self,
            session_type="mobile",
            env=self.env,
            metadata=self.metadata,
        )

        if self.platform not in SUPPORTED_PLATFORMS:
            raise ValueError(f"Unsupported platform: {self.platform}")
        self._reset_state()

    # -------------------------------------------------------------------------
    # BaseSession abstract methods
    # -------------------------------------------------------------------------
    def open(self) -> None:
        """Open/initialize the mobile app session."""
        self.launch_app()

    def close(self) -> None:
        """Close/cleanup the mobile app session."""
        self.close_app()

    def dump_state(self) -> Dict[str, Any]:
        """Snapshot of current session state for debugging/reporting."""
        return {
            "session_type": self.session_type,
            "env": self.env,
            "platform": self.platform,
            "app_launched": self.app_launched,
            "current_screen": self.current_screen,
            "state": self.state.copy(),
            "metadata": self.metadata.copy(),
        }

    # -------------------------------------------------------------------------
    # Session/App lifecycle
    # -------------------------------------------------------------------------
    def launch_app(self):
        self.app_launched = True
        self.current_screen = "welcome"
        self._reset_state()

    def close_app(self):
        self.app_launched = False

    # -------------------------------------------------------------------------
    # Element interaction API
    # -------------------------------------------------------------------------
    def _id(self, ios_id: str, android_id: str) -> str:
        return ios_id if self.platform == "ios" else android_id

    def is_visible(self, element_id: str) -> bool:
        # Visibility based on current screen and known elements
        mapping = {
            "welcome": {"login_button_ios", "login_button_android"},
            "login": {
                "email_input_ios",
                "password_input_ios",
                "login_button_ios",
                "terms_and_conditions_check_box_ios",
                "email_input_android",
                "password_input_android",
                "login_button_android",
                "terms_and_conditions_check_box_android",
            },
            "live_stream": {
                "live_stream_container_ios",
                "stream_status_label_ios",
                "live_stream_container_android",
                "stream_status_label_android",
            },
        }

        return self.app_launched and element_id in mapping.get(self.current_screen, set())

    def wait_for_visibility(self, element_id: str, timeout: float = 3.0, interval: float = 0.1) -> bool:
        """
        Simple polling wait for element visibility, similar to Appium waits.
        Raises AssertionError on timeout to keep tests deterministic.
        """
        end_time = time.time() + timeout
        while time.time() < end_time:
            if self.is_visible(element_id):
                return True
            time.sleep(interval)
        raise AssertionError(f"Element not visible after {timeout}s on '{self.current_screen}': {element_id}")

    def click(self, element_id: str):
        if not self.is_visible(element_id):
            raise AssertionError(f"Element not visible on '{self.current_screen}': {element_id}")

        # Navigation rules
        if element_id in {"login_button_ios", "login_button_android"} and self.current_screen == "welcome":
            self.current_screen = "login"
        elif element_id in {"login_button_ios", "login_button_android"} and self.current_screen == "login":
            self._attempt_login()

    def type(self, element_id: str, text: str):
        if not self.is_visible(element_id):
            raise AssertionError(f"Element not visible on '{self.current_screen}': {element_id}")

        if element_id in {"email_input_ios", "email_input_android"}:
            self.state["email"] = text
        elif element_id in {"password_input_ios", "password_input_android"}:
            self.state["password"] = text
        else:
            raise AssertionError(f"Unsupported input element: {element_id}")

    def set_checkbox(self, element_id: str, checked: bool):
        if not self.is_visible(element_id):
            raise AssertionError(f"Element not visible on '{self.current_screen}': {element_id}")

        if element_id in {"terms_and_conditions_check_box_ios", "terms_and_conditions_check_box_android"}:
            self.state["terms"] = bool(checked)
        else:
            raise AssertionError(f"Unsupported checkbox element: {element_id}")

    def get_text(self, element_id: str) -> str:
        if not self.is_visible(element_id):
            raise AssertionError(f"Element not visible on '{self.current_screen}': {element_id}")

        if element_id in {"stream_status_label_ios", "stream_status_label_android"}:
            return self.state.get("stream_status", "") or ""
        raise AssertionError(f"Unsupported label element: {element_id}")

    # -------------------------------------------------------------------------
    # Internal helpers
    # -------------------------------------------------------------------------
    def _reset_state(self):
        self.state = {
            "email": None,
            "password": None,
            "terms": False,
            "stream_status": "",  # becomes "streaming" after success
        }

    def _attempt_login(self):
        valid_email = self.state.get("email") in {"demo_app1@nanit.com", "demo_app2@nanit.com"}
        valid_password = self.state.get("password") in {"12341234", "12344321"}
        terms_ok = self.state.get("terms") is True

        if valid_email and valid_password and terms_ok:
            self.current_screen = "live_stream"
            self.state["stream_status"] = "streaming"
        else:
            # remain on login screen; could set an error message if needed
            self.state["stream_status"] = "login_failed"
