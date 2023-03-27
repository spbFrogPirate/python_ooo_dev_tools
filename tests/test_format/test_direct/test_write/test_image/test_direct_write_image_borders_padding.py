from __future__ import annotations
import pytest
from typing import cast
from pathlib import Path

if __name__ == "__main__":
    pytest.main([__file__])

import uno
from ooodev.format.writer.direct.image.borders import Padding
from ooodev.format.writer.direct.image.options import Names
from ooodev.utils.gui import GUI
from ooodev.utils.lo import Lo
from ooodev.office.write import Write
from ooodev.utils.images_lo import ImagesLo


def test_write(loader, fix_image_path) -> None:
    # delay = 0 if Lo.bridge_connector.headless else 3_000
    delay = 0

    doc = Write.create_doc()
    if not Lo.bridge_connector.headless:
        GUI.set_visible()
        Lo.delay(500)
        GUI.zoom(GUI.ZoomEnum.ENTIRE_PAGE)
    try:
        im_fnm = cast(Path, fix_image_path("skinner.png"))
        cursor = Write.get_cursor(doc)

        img_size = ImagesLo.get_size_100mm(im_fnm=im_fnm)
        style_names = Names(name="skinner", desc="Skinner Pointing", alt="Pointer")

        amt = 2.3
        style = Padding(all=amt)
        _ = Write.add_image_link(
            doc=doc,
            cursor=cursor,
            fnm=im_fnm,
            width=img_size.Width,
            height=img_size.Height,
            styles=(style_names, style),
        )

        graphics = Write.get_graphic_links(doc=doc)
        assert graphics is not None
        assert graphics.hasByName(style_names.prop_name)
        graphic = graphics.getByName(style_names.prop_name)

        f_style = Padding.from_obj(graphic)
        assert f_style.prop_left.value == pytest.approx(amt, rel=1e-2)
        assert f_style.prop_right.value == pytest.approx(amt, rel=1e-2)
        assert f_style.prop_top.value == pytest.approx(amt, rel=1e-2)
        assert f_style.prop_bottom.value == pytest.approx(amt, rel=1e-2)

        Lo.delay(delay)
    finally:
        Lo.close_doc(doc)