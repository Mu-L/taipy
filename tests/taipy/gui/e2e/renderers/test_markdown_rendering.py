from importlib import util

if util.find_spec("playwright"):
    from playwright._impl._page import Page

from taipy.gui import Gui


def test_markdown_render_with_style(page: "Page", gui: Gui, helpers):
    markdown_content = """
<|Hey|id=text1|>
<|There|id=text1|classname=custom-text|>
"""
    style = """
.taipy-text {
    color: green;
}
.custom-text {
    color: blue;
}
"""
    gui.add_page("page1", markdown_content, style=style)
    helpers.run_e2e(gui)
    page.goto("/page1")
    page.expect_websocket()
    page.wait_for_selector("#text1")
    assert (
        page.evaluate('window.getComputedStyle(document.querySelector("#text1"), null).getPropertyValue("color")')
        == "rgb(0, 128, 0)"
    )
    assert (
        page.evaluate('window.getComputedStyle(document.querySelector("#text2"), null).getPropertyValue("color")')
        == "rgb(0, 0, 255)"
    )
