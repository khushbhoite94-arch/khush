from pathlib import Path
import json

from app.automation.browser import BrowserManager

OUTPUT = Path("inspection")
OUTPUT.mkdir(exist_ok=True)

browser = BrowserManager()

try:
    browser.start()
    browser.open_tradingview()

    page = browser.page

    page.wait_for_timeout(5000)

    # HTML
    (OUTPUT / "dom.html").write_text(
        page.content(),
        encoding="utf-8"
    )

    # Screenshot
    page.screenshot(
        path=str(OUTPUT / "page.png"),
        full_page=False
    )

    page.screenshot(
        path=str(OUTPUT / "page_full.png"),
        full_page=True
    )

    # Buttons
    buttons = page.locator("button").evaluate_all("""
(nodes) => nodes.map(node => ({
    text: node.innerText,
    ariaLabel: node.getAttribute("aria-label"),
    role: node.getAttribute("role"),
    id: node.id,
    className: node.className
}))
""")

    with open(OUTPUT / "buttons.json", "w", encoding="utf-8") as f:
        json.dump(buttons, f, indent=4, ensure_ascii=False)

    # Inputs
    inputs = page.locator("input").evaluate_all("""
(nodes) => nodes.map(node => ({
    type: node.type,
    placeholder: node.placeholder,
    ariaLabel: node.getAttribute("aria-label"),
    id: node.id,
    name: node.name
}))
""")

    with open(OUTPUT / "inputs.json", "w", encoding="utf-8") as f:
        json.dump(inputs, f, indent=4, ensure_ascii=False)

    # Links
    links = page.locator("a").evaluate_all("""
(nodes) => nodes.map(node => ({
    text: node.innerText,
    href: node.href
}))
""")

    with open(OUTPUT / "links.json", "w", encoding="utf-8") as f:
        json.dump(links, f, indent=4, ensure_ascii=False)

    # Page title
    (OUTPUT / "title.txt").write_text(
        page.title(),
        encoding="utf-8"
    )

    print("\nInspection completed successfully.\n")
    input("Press ENTER to close...")

finally:
    browser.stop()