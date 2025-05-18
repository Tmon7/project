import pytest
from playwright.sync_api import sync_playwright


@pytest.fixture()
def browser():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=False, slow_mo=1000
        ) 
        yield browser
        browser.close()


@pytest.fixture()
def page(browser):
    page = browser.new_page()
    yield page
    page.close()




def test_invalid_login_without_password(page):
    xpath_cookie_refuse ='//*[@id="frm-consentPopUp-consentForm"]/p[3]/button[1]'
    id_email_input = "#frm-loginForm-login"
    id_password_input = "#frm-loginForm-password"
    id_submit_button = "#frm-loginForm > p:nth-child(7) > button"
    id_warning_message = "#frm-loginForm > p:nth-child(6) > label.inp-error.pdforms-message"

    page.goto("https://www.superzoo.cz/uzivatel-prihlaseni/")

    # Odmietnutie cookies
    cookie_refuse_button=page.locator(xpath_cookie_refuse)
    cookie_refuse_button.click()

    # Vyplníme len e-mail, heslo necháme prázdne
    page.fill(id_email_input, "test@example.com")
    page.fill(id_password_input, "")  # nepíše sa nič

    # Klikneme na tlačidlo "Přihlásit se"
    page.click(id_submit_button)

    # Počkáme na výskyt chybového hlásenia
    page.wait_for_selector(id_warning_message)

    # Overíme, že sa zobrazí text "Toto pole je povinné"
    warning_text = page.locator(id_warning_message).inner_text()
    assert "Toto pole je povinné" in warning_text
