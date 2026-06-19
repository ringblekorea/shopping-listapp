"""Automated UI test for index.html (add / check / delete)."""
import pathlib
import sys
from playwright.sync_api import sync_playwright

HTML = pathlib.Path(__file__).parent / "index.html"
URL = HTML.as_uri()

results = []


def check(name, condition):
    status = "PASS" if condition else "FAIL"
    results.append((name, condition))
    print(f"[{status}] {name}")


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    # Start with a clean localStorage so the run is deterministic.
    page.goto(URL)
    page.evaluate("localStorage.clear()")
    page.reload()
    page.wait_for_load_state("networkidle")

    # --- Initial state ---
    check("empty message shown at start", page.locator("#empty").is_visible())
    check("list is empty at start", page.locator("#list li").count() == 0)

    # --- Add items ---
    for item in ["우유", "계란", "빵"]:
        page.fill("#input", item)
        page.click("button[type=submit]")

    check("3 items added", page.locator("#list li").count() == 3)
    check("empty message hidden after add", not page.locator("#empty").is_visible())
    check(
        "item text rendered correctly",
        page.locator("#list li .name").nth(0).inner_text() == "우유",
    )
    check("count shows 3 items / 3 remaining", "3개 항목 · 3개 남음" in page.inner_text("#count"))

    # --- Add via Enter key ---
    page.fill("#input", "버터")
    page.press("#input", "Enter")
    check("4th item added via Enter key", page.locator("#list li").count() == 4)

    # --- Empty input should not add ---
    page.fill("#input", "   ")
    page.click("button[type=submit]")
    check("blank input is ignored", page.locator("#list li").count() == 4)

    # --- Check (toggle done) ---
    first = page.locator("#list li").nth(0)
    first.locator("input[type=checkbox]").check()
    check("item gets 'done' class when checked", "done" in (first.get_attribute("class") or ""))
    check("remaining count drops to 3", "4개 항목 · 3개 남음" in page.inner_text("#count"))

    # --- Persistence across reload ---
    page.reload()
    page.wait_for_load_state("networkidle")
    check("items persist after reload", page.locator("#list li").count() == 4)
    check(
        "checked state persists after reload",
        page.locator("#list li").nth(0).locator("input[type=checkbox]").is_checked(),
    )

    # --- Delete a single item ---
    page.locator("#list li").nth(0).locator(".delete").click()
    check("item count drops to 3 after delete", page.locator("#list li").count() == 3)
    check(
        "correct item deleted (우유 gone)",
        "우유" not in page.inner_text("#list"),
    )

    # --- Clear completed ---
    # check two items, then clear done
    page.locator("#list li").nth(0).locator("input[type=checkbox]").check()
    page.locator("#list li").nth(1).locator("input[type=checkbox]").check()
    page.click("#clearDone")
    check("clear-done removes checked items", page.locator("#list li").count() == 1)

    # --- Delete all -> empty message returns ---
    while page.locator("#list li").count() > 0:
        page.locator("#list li").nth(0).locator(".delete").click()
    check("empty message returns when all deleted", page.locator("#empty").is_visible())

    page.screenshot(path="test_result.png", full_page=True)
    browser.close()

passed = sum(1 for _, ok in results if ok)
total = len(results)
print(f"\n=== {passed}/{total} checks passed ===")
sys.exit(0 if passed == total else 1)
