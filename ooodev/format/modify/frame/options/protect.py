"""
Module for Fill Transparency.

.. versionadded:: 0.9.0
"""
from __future__ import annotations
from typing import cast
import uno

from ..frame_style_base_multi import FrameStyleBaseMulti
from ....writer.style.frame.style_frame_kind import StyleFrameKind as StyleFrameKind
from ....direct.frame.options.protect import Protect as DirectProtect


class Protect(FrameStyleBaseMulti):
    """
    Frame Style Options Protect.

    .. versionadded:: 0.9.0
    """

    def __init__(
        self,
        *,
        size: bool | None = None,
        postiion: bool | None = None,
        content: bool | None = None,
        style_name: StyleFrameKind | str = StyleFrameKind.FRAME,
        style_family: str = "FrameStyles",
    ) -> None:
        """
        Constructor

        Args:
            size (bool, optional): Specifies size protection.
            postiion (bool, optional): Specifies postiion protection.
            content (bool, optional): Specifies content protection.
            style_name (StyleFrameKind, str, optional): Specifies the Frame Style that instance applies to. Deftult is Default Frame Style.
            style_family (str, optional): Style family. Defatult ``FrameStyles``.

        Returns:
            None:
        """

        direct = DirectProtect(size=size, postiion=postiion, content=content)
        direct._prop_parent = self
        super().__init__()
        self._style_name = str(style_name)
        self._style_family_name = style_family
        self._set_style("direct", direct, *direct.get_attrs())

    @classmethod
    def from_style(
        cls,
        doc: object,
        style_name: StyleFrameKind | str = StyleFrameKind.FRAME,
        style_family: str = "FrameStyles",
    ) -> Protect:
        """
        Gets instance from Document.

        Args:
            doc (object): UNO Documnet Object.
            style_name (StyleFrameKind, str, optional): Specifies the Frame Style that instance applies to. Deftult is Default Frame Style.
            style_family (str, optional): Style family. Defatult ``FrameStyles``.

        Returns:
            Protect: ``Protect`` instance from style properties.
        """
        inst = super(Protect, cls).__new__(cls)
        inst.__init__(style_name=style_name, style_family=style_family)
        direct = DirectProtect.from_obj(inst.get_style_props(doc))
        direct._prop_parent = inst
        inst._set_style("direct", direct, *direct.get_attrs())
        return inst

    @property
    def prop_style_name(self) -> str:
        """Gets/Sets property Style Name"""
        return self._style_name

    @prop_style_name.setter
    def prop_style_name(self, value: str | StyleFrameKind):
        self._style_name = str(value)

    @property
    def prop_inner(self) -> DirectProtect:
        """Gets Inner Protect instance"""
        try:
            return self._direct_inner
        except AttributeError:
            self._direct_inner = cast(DirectProtect, self._get_style_inst("direct"))
        return self._direct_inner
