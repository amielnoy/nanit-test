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
@pytest.mark.mobile_ui
@allure.feature("Mobile UI")
@allure.story("Login and navigate till stream status Flow")
@allure.title("mobile stream status validation")
def test_mobile_stream_status(email, password, mobile_session: MobileSession, api_streaming):
    step = AllureStep("Mobile Stream Status")
    masked_email = f"{email[:2]}***@{email.split('@')[-1]}"
    allure.dynamic.parameter("email", masked_email)
    allure.dynamic.parameter("password", "*" * len(password))
    if allure:
        allure.dynamic.title(f"mobile stream status validation for {masked_email}")

    with step("Log test configuration"):
        print(f"Testing login with: {masked_email} / {'*' * len(password)}")

        masked_email = f"{email[:2]}***@{email.split('@')[-1]}"
        step.attach_text("Login email", masked_email)

    with step("Open Welcome page and validate visibility"):
        welcome = get_welcome_page(mobile_session)
        assert welcome.is_visible(), "Welcome screen should show login button"

    with step("Tap login on Welcome page"):
        welcome.tap_login()

    with step("Open Login page and validate visibility"):
        login = get_login_page(mobile_session)
        assert login.is_visible(), "Login screen should be visible after tapping login"

    with step("Fill login form and submit"):
        login.enter_email(email)
        login.enter_password(password)
        login.accept_terms()
        login.tap_login()

    with step("Validate Live Stream screen is visible and status == 'streaming'"):
        live = get_live_stream_page(mobile_session)
        assert live.is_visible(), "Live Stream screen should be visible after login"

        ui_status = live.get_stream_status()
        step.attach_text("UI streaming status", ui_status)
        assert ui_status == "streaming"

    with step("Final confirmation message"):
        masked_email = f"{email[:2]}***@{email.split('@')[-1]}"
        message = (
            "Test passed: Mobile login completed successfully and "
            "stream status = 'streaming' on mobile app "
            f"for user {masked_email}."
        )
        print(message)
        step.attach_text("Final Result", message)
