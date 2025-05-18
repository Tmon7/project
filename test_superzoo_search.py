import pytest
from playwright.sync_api import sync_playwright, expect


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

@pytest.mark.parametrize("search_term", [
    "pamlsky",
    "granule",
    "krmivo"
])

def test_search(page,search_term):
    xpath_cookie_refuse ='//*[@id="frm-consentPopUp-consentForm"]/p[3]/button[1]'
    id_search_box ="#frm-searchBox-searchForm-query"

    page.goto("https://superzoo.cz/")

    # Odmietnutie cookies
    cookie_refuse_button=page.locator(xpath_cookie_refuse)
    cookie_refuse_button.click()

    # Prevedieme vyhľadanie produktu
    search_box=page.locator(id_search_box)
    search_box.fill(search_term)
    search_box.press("Enter")

    # Počkáme a overíme, či stránka zobrazuje vyhľadávaný produkt
    page.wait_for_timeout(4000)
    assert search_term in page.url
    expect(page.locator("body")).to_contain_text(search_term)

