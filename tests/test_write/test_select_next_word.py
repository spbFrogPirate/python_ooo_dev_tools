import pytest

if __name__ == "__main__":
    pytest.main([__file__])

from ooodev.loader.lo import Lo
from ooodev.office.write import Write
from ooodev.gui.gui import GUI

LAST_PARA = """
At three o'clock precisely I was at Baker Street, but Holmes had not yet returned. The landlady informed me that he had left the house shortly after eight o'clock in the morning. I sat down beside the fire, however, with the intention of awaiting him, however long he might be.
"""


def test_select_next_word(loader, copy_fix_writer):

    # text file opens with each new line being considered a paragraph break.

    # test require Writer be visible
    visible = True
    delay = 300
    test_doc = copy_fix_writer("scandalStart.odt")
    doc = Write.open_doc(test_doc, loader)
    try:
        if visible:
            GUI.set_visible(visible, doc)

        # make sure when doc opens cursor is set to start
        vc = Write.get_view_cursor(doc)
        vc.gotoStart(False)
        vc.collapseToStart()

        assert Write.is_anything_selected(doc) == False
        Write.select_next_word(doc)
        assert Write.is_anything_selected(doc)

        s = Write.get_selected_text_str(doc)
        assert s == "Title: "
        Lo.delay(delay)

        Write.select_next_word(doc)
        s = Write.get_selected_text_str(doc)
        assert s == "A "
        Lo.delay(delay)

        # no deselect
        Write.select_next_word(doc)
        s = Write.get_selected_text_str(doc)
        assert s == "Scandal "
        Lo.delay(delay)

        # jump to last paragraph
        vc.goRight(554, False)
        words = LAST_PARA.split()
        for i in range(50):  # 50 Max
            Write.select_next_word(doc)
            s = Write.get_selected_text_str(doc).strip()
            assert s == words[i]
            Lo.delay(100)
        # vc.goRight(10, True)

        Lo.delay(delay)
    finally:
        Lo.close_doc(doc, False)
