import pytest
import allure

from infra.mobile_session import MobileSession
from mobile_pages.factory import (
    get_welcome_page,
    get_login_page,
    get_live_stream_page,
)
from infra.allure_utils import AllureStep
from infra.test_data_loader import load_login_users


@pytest.mark.parametrize(
    "email,password",
    [(u["email"], u["password"]) for u in load_login_users()]
)
@pytest.mark.e2e_api_integrated
@allure.feature("Mobile Streaming")
@allure.story("Login and Live Stream Status Validation")
@allure.title("Stream status is consistent between UI and backend")
def test_mobile_and_backend_stream_status_are_consistent(
    email,
    password,
    mobile_session: MobileSession,
    api_streaming,
):
    step = AllureStep("Mobile & Backend Stream Status")
    masked_email = f"{email[:2]}***@{email.split('@')[-1]}"
    allure.dynamic.parameter("email", masked_email)
    allure.dynamic.parameter("password", "*" * len(password))

    with step("Print test credentials (masked password)"):
        print(f"Testing login with {masked_email} / {'*' * len(password)}")
        step.attach_text("Test email", masked_email)

    with step("Open Welcome page and validate visibility"):
        welcome = get_welcome_page(mobile_session)
        assert welcome.is_visible(), "Welcome screen should show login button"

    with step("Navigate from Welcome to Login screen"):
        welcome.tap_login()
        login = get_login_page(mobile_session)
        assert login.is_visible(), "Login screen should be visible after tapping login"

    with step("Fill login form and submit"):
        login.enter_email(email)
        login.enter_password(password)
        login.accept_terms()
        login.tap_login()

    with step("Validate Live Stream screen is visible and status is 'streaming' on UI"):
        live = get_live_stream_page(mobile_session)
        assert live.is_visible(), "Live Stream screen should be visible after successful login"

        ui_status = live.get_stream_status()
        step.attach_text("UI streaming status (first check)", ui_status)
        assert ui_status == "streaming", "error streaming not detected on mobile app"

    with step("Validate streaming status via backend API and compare with UI"):
        api_streaming_validator = mobile_session.api_streaming_validator
        api_streaming_validator.set_network_condition(api_streaming, "normal")

        backend_metrics = api_streaming_validator.fetch_metrics(api_streaming)
        backend_status = backend_metrics.get("status")
        ui_status_final = live.get_stream_status()

        step.attach_text("Backend streaming status", backend_status)
        step.attach_text("UI streaming status (before final assert)", ui_status)
        step.attach_text("UI streaming status (final)", ui_status_final)

        assert ui_status_final == backend_status, (
            "error streaming status is not identical in mobile ui & on streaming"
        )

    with step("Final log – Test passed"):
        masked_email = f"{email[:2]}***@{email.split('@')[-1]}"
        msg = (
            "Test passed: Mobile login and stream status are the same on mobile ui & on streaming "
            f"for user {masked_email}."
        )
        print(msg)
        step.attach_text("Final result", msg)
