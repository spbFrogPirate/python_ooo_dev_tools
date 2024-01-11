"""DrawPages class for Draw documents."""
from __future__ import annotations
from typing import TYPE_CHECKING, TypeVar, Generic
import contextlib
import uno
from com.sun.star.drawing import XDrawPage

from ooodev.adapter.container.name_access_partial import NameAccessPartial
from ooodev.adapter.drawing.draw_pages_comp import DrawPagesComp
from ooodev.draw import draw_page as mDrawPage
from ooodev.exceptions import ex as mEx
from ooodev.utils import lo as mLo
from ooodev.utils import info as mInfo
from ooodev.utils.partial.qi_partial import QiPartial

from ooodev.proto.component_proto import ComponentT

if TYPE_CHECKING:
    from com.sun.star.drawing import XDrawPages

_T = TypeVar("_T", bound="ComponentT")


class DrawPages(Generic[_T], DrawPagesComp, NameAccessPartial, QiPartial):
    """
    Class for managing Draw Pages.
    """

    def __init__(self, owner: _T, slides: XDrawPages) -> None:
        """
        Constructor

        Args:
            owner (DrawDoc): Owner Document
            sheet (XDrawPages): Document Pages.
        """
        self.__owner = owner
        DrawPagesComp.__init__(self, slides)  # type: ignore
        # The API does not show that DrawPages implements XNameAccess, but it does.
        NameAccessPartial.__init__(self, component=slides, interface=None)  # type: ignore
        QiPartial.__init__(self, component=slides, lo_inst=mLo.Lo.current_lo)
        self._current_index = 0

    def __getitem__(self, _itm: int | str) -> mDrawPage.DrawPage[_T]:
        if isinstance(_itm, str):
            return self.get_by_name(_itm)
        if _itm < 0:
            _itm = len(self) + _itm
            if _itm < 0:
                raise IndexError("list index out of range")
        return self.get_by_index(idx=_itm)

    def __len__(self) -> int:
        return self.component.getCount()

    def __iter__(self):
        self._current_index = 0
        return self

    def __next__(self) -> mDrawPage.DrawPage[_T]:
        if self._current_index >= len(self):
            self._current_index = 0
            raise StopIteration
        self._current_index += 1
        return self[self._current_index - 1]

    def __delitem__(self, _item: int | str | mDrawPage.DrawPage[_T] | XDrawPage) -> None:
        # Delete slide by index, name, or object
        # Usage:
        # del doc.slides[-1]
        # assert len(doc.slides) == 8

        # last_slide = doc.slides[-1]
        # del doc.slides[last_slide.get_name()]
        # assert len(doc.slides) == 7

        # last_slide = doc.slides[-1]
        # del doc.slides[last_slide]
        # assert len(doc.slides) == 6

        # last_slide = doc.slides[-1]
        # del doc.slides[last_slide.component] # type: ignore
        # assert len(doc.slides) == 5
        if mInfo.Info.is_instance(_item, int):
            self.delete_slide(_item)
        elif mInfo.Info.is_instance(_item, str):
            slide = super().get_by_name(_item)
            if slide is None:
                raise mEx.MissingNameError(f"Unable to find slide with name '{_item}'")
            super().remove(slide)
        elif mInfo.Info.is_instance(_item, mDrawPage.DrawPage):
            super().remove(_item.component)
        elif mInfo.Info.is_instance(_item, XDrawPage):
            super().remove(_item)
        else:
            raise TypeError(f"Unsupported type: {type(_item)}")

    def insert_slide(self, idx: int) -> mDrawPage.DrawPage[_T]:
        """
        Inserts a slide at the given position in the document

        Args:
            idx (int): Index, can be a negative value to insert from the end of the document.
                For example, -1 will insert at the end of the document.

        Raises:
            DrawPageMissingError: If unable to get pages.
            DrawPageError: If any other error occurs.

        Returns:
            DrawPage: New slide that was inserted.
        """
        if idx < 0:
            idx = len(self) + idx
            if idx < 0:
                raise IndexError("list index out of range")
        return mDrawPage.DrawPage(self.owner, self.component.insertNewByIndex(idx))

    def delete_slide(self, idx: int) -> bool:
        """
        Deletes a slide

        Args:
            idx (int): Index. Can be a negative value to delete from the end of the document.
                For example, -1 will delete the last slide.

        Returns:
            bool: ``True`` on success; Otherwise, ``False``
        """
        if idx < 0:
            idx = len(self) + idx
            if idx < 0:
                raise IndexError("list index out of range")
        with contextlib.suppress(Exception):
            # get the slide as UNO object and remove it
            result = super().get_by_index(idx)
            if result is None:
                return False
            self.remove(result)
            return True
        return False

    # region XNameAccess overrides

    def get_by_name(self, name: str) -> mDrawPage.DrawPage[_T]:
        """
        Gets the element with the specified name.

        Args:
            name (str): The name of the element.

        Raises:
            MissingNameError: If unable to find slide with name.

        Returns:
            DrawPage[DrawDoc]: The drawpage with the specified name.
        """
        if not self.has_by_name(name):
            raise mEx.MissingNameError(f"Unable to find slide with name '{name}'")

        result = super().get_by_name(name)
        return mDrawPage.DrawPage(owner=self.owner, component=result)

    # endregion XNameAccess overrides

    # region XIndexAccess overrides

    def get_by_index(self, idx: int) -> mDrawPage.DrawPage[_T]:
        """
        Gets the element with the specified index.

        Args:
            idx (int): The index of the element. Idx can be a negative value to get from the end of the document.
                For example, -1 will get the last slide.

        Raises:
            IndexError: If unable to find slide with index.

        Returns:
            DrawPage[DrawDoc]: The drawpage with the specified index.
        """
        if idx < 0:
            idx = len(self) + idx
            if idx < 0:
                raise IndexError("Index out of range")
        if idx >= len(self):
            raise IndexError(f"Index out of range: '{idx}'")

        result = super().get_by_index(idx)
        return mDrawPage.DrawPage(owner=self.owner, component=result)

    # endregion XIndexAccess overrides

    # region XDrawPages overrides
    def insert_new_by_index(self, idx: int) -> mDrawPage.DrawPage[_T]:
        """
        Creates and inserts a new DrawPage or MasterPage into this container.

        Args:
            idx (int): The index at which the new page will be inserted.
                ``idx`` can be a negative value to insert from the end of the document.
                For example, ``-1`` will insert at the end of the document.

        Returns:
            DrawPage: The new page.
        """
        if idx >= len(self):
            # if index is greater than the number of slides, then insert at the end
            idx = -1
        if idx < 0:
            idx = len(self) + idx
            if idx < 0:
                raise IndexError("Index out of range")
        result = super().insert_new_by_index(idx)
        return mDrawPage.DrawPage(owner=self.owner, component=result)

    # endregion XDrawPages overrides

    # region Properties
    @property
    def owner(self) -> _T:
        """
        Returns:
            _T: Draw or Impress document.
        """
        return self.__owner

    # endregion Properties