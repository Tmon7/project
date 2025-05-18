import pytest
from playwright.sync_api import sync_playwright,expect


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


def test_button_registration(page):
    xpath_cookie_refuse = '//*[@id="frm-consentPopUp-consentForm"]/p[3]/button[1]'
    xpath_registration_button = '//*[@id="top"]/main/div[1]/div/section[1]/p/a'

    page.goto("https://superzoo.cz/")

    # Odmietnutie cookies
    cookie_refuse_button = page.locator(xpath_cookie_refuse)
    cookie_refuse_button.click()

    # Kliknutie na registračné tlačidlo
    registration_button = page.locator(xpath_registration_button)
    registration_button.click()

    # Overenie úspešného prechodu na registračnú stránku – napríklad nadpis
    registration_heading = page.locator("text=Registrace")
    expect(registration_heading).to_be_visible()

    