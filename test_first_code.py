import os

from dotenv import load_dotenv
from playwright.sync_api import Page, expect

load_dotenv()
BASE_URL = os.getenv("UI_BASE")


def test_first_code(page: Page):
    page.goto(BASE_URL)
    page.locator("(//div/a[@class='us-link'])[1]").click()
    page.get_by_text("Shop Top 100 Deals", exact=True).click()
    expect(page.get_by_role("heading", name="Featured Deals")).to_be_visible()

    product_deals = page.locator("div.wf-offer-content")

    names = []
    for i, p in enumerate(product_deals.all()):
        p.scroll_into_view_if_needed()
        name = p.locator("h3[class='heading product-title']").inner_text()
        assert name.strip(), f"Card {i + 1} has an empty title"
        names.append(f"{i + 1}.{name}")

    with open("product_names.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(names))
