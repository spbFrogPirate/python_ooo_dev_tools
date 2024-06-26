.. _help_writer_format_direct_char_font_effects:

Write Direct Character FontEffects Class
========================================

.. contents:: Table of Contents
    :local:
    :backlinks: none
    :depth: 2

The :py:class:`ooodev.format.writer.direct.char.font.FontEffects` class gives you the same options
as Writer's Font Effects Dialog, but without the dialog. as seen in :numref:`ss_writer_dialog_char_font_effects`.

.. cssclass:: screen_shot invert

    .. _ss_writer_dialog_char_font_effects:
    .. figure:: https://user-images.githubusercontent.com/4193389/229378606-e2f3181e-4281-4485-8a37-da0b560f9831.png
        :alt: Writer dialog Character font
        :figclass: align-center
        :width: 450px

        Writer dialog: Character font


Setting the style
-----------------

.. tabs::

    .. code-tab:: python
        :emphasize-lines: 17, 18, 19, 20

        from ooodev.format.writer.direct.char.font import (
            FontOnly, FontEffects, FontLine, FontUnderlineEnum
        )
        from ooodev.office.write import Write
        from ooodev.utils.color import CommonColor
        from ooodev.gui import GUI
        from ooodev.loader.lo import Lo

        def main() -> int:
            with Lo.Loader(Lo.ConnectPipe()):
                doc = Write.create_doc()
                GUI.set_visible(doc=doc)
                Lo.delay(300)
                GUI.zoom(GUI.ZoomEnum.PAGE_WIDTH)
                cursor = Write.get_cursor(doc)
                font_style = FontOnly(name="Liberation Serif", size=20)
                font_effects = FontEffects(
                    color=CommonColor.RED,
                    underline=FontLine(line=FontUnderlineEnum.SINGLE, color=CommonColor.BLUE),
                    shadowed=True,
                )

                Write.append_para(
                    cursor=cursor, text="Hello World!", styles=[font_style, font_effects]
                )
                Lo.delay(1_000)

                Lo.close_doc(doc)

            return 0

        if __name__ == "__main__":
            sys.exit(main())

    .. only:: html

        .. cssclass:: tab-none

            .. group-tab:: None

Running the above code will produce the following output in :numref:`229379242-a98c30ee-1b94-4f51-8aa5-7afbf9635b24`.

.. cssclass:: screen_shot

    .. _229379242-a98c30ee-1b94-4f51-8aa5-7afbf9635b24:
    .. figure:: https://user-images.githubusercontent.com/4193389/229379242-a98c30ee-1b94-4f51-8aa5-7afbf9635b24.png
        :alt: Writer dialog Character font 20pt
        :figclass: align-center
        :width: 450px

        Hello World with 20pt font, red color and underline blue color.

The results can be seen in dialog show in  :numref:`229383701-84fca154-24a8-4724-b489-ff8b57d4bfa2`.

.. cssclass:: screen_shot

    .. _229383701-84fca154-24a8-4724-b489-ff8b57d4bfa2:
    .. figure:: https://user-images.githubusercontent.com/4193389/229383701-84fca154-24a8-4724-b489-ff8b57d4bfa2.png
        :alt: Writer dialog Character Font Effects
        :figclass: align-center
        :width: 450px

        Writer dialog: Character Font Effects

Getting the font effects from the document
-------------------------------------------

Continuing from the code example above, we can get the font effect from the document.

A paragraph cursor object is used to select the first paragraph in the document.
The paragraph cursor is then used to get the style.

.. tabs::

    .. code-tab:: python
        :emphasize-lines: 7

        # ... other code

        para_cursor = Write.get_paragraph_cursor(cursor)
        para_cursor.gotoPreviousParagraph(False)
        para_cursor.gotoEndOfParagraph(True)

        font_effects = FontEffects.from_obj(para_cursor)

        assert font_effects.prop_color == CommonColor.RED
        assert font_effects.prop_underline.line == FontUnderlineEnum.SINGLE
        assert font_effects.prop_underline.color == CommonColor.BLUE
        para_cursor.gotoEnd(False)

    .. only:: html

        .. cssclass:: tab-none

            .. group-tab:: None

Related Topics
--------------

.. seealso::

    .. cssclass:: ul-list

        - :ref:`help_format_format_kinds`
        - :ref:`help_format_coding_style`
        - :ref:`help_writer_format_direct_char_font_only`
        - :ref:`help_writer_format_direct_char_font`
        - :ref:`help_writer_format_modify_char_font_effects`
        - :ref:`help_writer_format_modify_para_font_effects`
        - :ref:`help_calc_format_direct_cell_font_effects`
        - :py:class:`~ooodev.gui.GUI`
        - :py:class:`~ooodev.loader.Lo`
        - :py:class:`ooodev.format.writer.direct.char.font.FontEffects`
        - :py:class:`ooodev.format.writer.direct.char.font.FontOnly`
        - :py:class:`ooodev.format.writer.direct.char.font.FontLine`