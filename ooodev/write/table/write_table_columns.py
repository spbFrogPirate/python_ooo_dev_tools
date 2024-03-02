from __future__ import annotations
from typing import TYPE_CHECKING

from ooodev.adapter.text.table_columns_comp import TableColumnsComp
from ooodev.utils.partial.lo_inst_props_partial import LoInstPropsPartial
from ooodev.write.partial.write_doc_prop_partial import WriteDocPropPartial
from ooodev.write.table.partial.write_table_prop_partial import WriteTablePropPartial
from ooodev.utils import gen_util as mGenUtil

if TYPE_CHECKING:
    from com.sun.star.table import XTableColumns
    from ooodev.write.table.write_table import WriteTable


class WriteTableColumns(WriteDocPropPartial, WriteTablePropPartial, TableColumnsComp, LoInstPropsPartial):
    """Represents writer table columns."""

    def __init__(self, owner: WriteTable, component: XTableColumns) -> None:
        """
        Constructor

        Args:
            component (XTableColumns): UNO object that supports ``com.sun.star.text.TableColumns`` service.
        """
        WriteDocPropPartial.__init__(self, obj=owner.write_doc)  # type: ignore
        WriteTablePropPartial.__init__(self, obj=owner)
        LoInstPropsPartial.__init__(self, lo_inst=owner.lo_inst)
        TableColumnsComp.__init__(self, component=component)  # type: ignore

    def _get_index(self, idx: int, allow_greater: bool = False) -> int:
        """
        Gets the index.

        Args:
            idx (int): Index of sheet. Can be a negative value to index from the end of the list.
            allow_greater (bool, optional): If True and index is greater then the number of
                sheets then the index becomes the next index if sheet were appended. Defaults to False.

        Returns:
            int: Index value.
        """
        count = len(self)
        return mGenUtil.Util.get_index(idx, count, allow_greater)

    # region XTableColumns Overrides
    def insert_by_index(self, idx: int, count: int = 1) -> None:
        """
        Inserts a new column at the specified index.

        Args:
            idx (int): The index at which the column will be inserted. A value of ``-1`` will append the column at the end.
            count (int, optional): The number of columns to insert. Defaults to ``1``.
        """
        index = self._get_index(idx, True)
        self.component.insertByIndex(index, count)

    def remove_by_index(self, idx: int, count: int = 1) -> None:
        """
        Removes columns from the specified idx.

        Args:
            idx (int): The index at which the column will be removed. A value of ``-1`` will remove the last column.
            count (int, optional): The number of columns to remove. Defaults to ``1``.
        """
        index = self._get_index(idx)
        self.component.removeByIndex(index, count)

    # endregion XTableColumns Overrides
