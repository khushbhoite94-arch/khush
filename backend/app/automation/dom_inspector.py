"""
AEGIS AI
DOM Inspector
"""

import json
from pathlib import Path


class DOMInspector:

    def __init__(self, page):

        self.page = page

        self.output = Path("inspection")

        self.output.mkdir(exist_ok=True)

    # --------------------------------------------------

    def inspect(self):

        print("[AEGIS] Saving HTML...")

        html = self.page.content()

        (self.output / "dom.html").write_text(
            html,
            encoding="utf-8",
        )

        print("[AEGIS] Saving Screenshot...")

        self.page.screenshot(
            path=self.output / "chart.png",
            full_page=True,
        )

        print("[AEGIS] Saving Buttons...")

        buttons = self.page.locator("button").evaluate_all(
            """
            els => els.map(e => ({
                text: e.innerText,
                aria: e.getAttribute("aria-label"),
                title: e.getAttribute("title")
            }))
            """
        )

        with open(
            self.output / "buttons.json",
            "w",
            encoding="utf-8",
        ) as f:

            json.dump(
                buttons,
                f,
                indent=4,
            )

        print("[AEGIS] Saving Inputs...")

        inputs = self.page.locator("input").evaluate_all(
            """
            els => els.map(e => ({
                placeholder: e.placeholder,
                aria: e.getAttribute("aria-label"),
                type: e.type
            }))
            """
        )

        with open(
            self.output / "inputs.json",
            "w",
            encoding="utf-8",
        ) as f:

            json.dump(
                inputs,
                f,
                indent=4,
            )

        print("[AEGIS] Inspection Complete.")