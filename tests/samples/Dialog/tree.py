from __future__ import annotations
from typing import Any, cast, TYPE_CHECKING
import uno  # pylint: disable=unused-import
from ooo.dyn.awt.pos_size import PosSize
from ooo.dyn.awt.push_button_type import PushButtonType

from ooodev.dialog import Dialogs, BorderKind
from ooodev.dialog.msgbox import MsgBox, MessageBoxResultsEnum, MessageBoxType
from ooodev.dialog.search.tree_search import RuleDataInsensitive
from ooodev.dialog.search.tree_search import RuleTextInsensitive
from ooodev.dialog.search.tree_search import RuleTextRegex
from ooodev.dialog.search.tree_search.search_tree import SearchTree
from ooodev.events.args.event_args import EventArgs
from ooodev.office.calc import Calc
from ooodev.utils import lo as mLo
from ooodev.utils.gui import GUI


if TYPE_CHECKING:
    from ooodev.dialog.dl_control.ctl_tree import CtlTree
    from com.sun.star.awt import ActionEvent


class Tree:
    # pylint: disable=unused-argument
    def __init__(self) -> None:
        self._border_kind = BorderKind.BORDER_SIMPLE
        self._title = "Tree Example"
        self._width = 600
        self._height = 500
        self._btn_width = 100
        self._btn_height = 30
        self._margin = 4
        self._box_height = 30
        if self._border_kind != BorderKind.BORDER_3D:
            self._padding = 10
        else:
            self._padding = 14

        self._init_handlers()

        self._dialog = Dialogs.create_dialog(
            x=-1,
            y=-1,
            width=self._width,
            height=self._height,
            title=self._title,
        )
        # windows peer must be created before tree control is added; otherwise,
        # the tree control will not work correctly. Some nodes seem not be added or visible.
        _ = Dialogs.create_dialog_peer(self._dialog)

        self._ctl_tree = Dialogs.insert_tree_control(
            dialog_ctrl=self._dialog.control,
            x=self._margin,
            y=self._padding,
            width=self._width - (self._margin * 2),
            height=self._height - (self._padding * 3) - self._btn_height,
            border=self._border_kind,
        )
        # dm = self._ctl_tree.data_model
        self._root1 = self._ctl_tree.create_root(display_value="Root 1")
        if self._root1:
            _ = self._ctl_tree.add_sub_node(parent_node=self._root1, display_value="Node 1")
            _ = self._ctl_tree.add_sub_node(parent_node=self._root1, display_value="Node 3")
            _ = self._ctl_tree.add_sub_node(parent_node=self._root1, display_value="Node 3")
        self._root2 = self._ctl_tree.create_root(display_value="Root 2")
        if self._root2:
            _ = self._ctl_tree.add_sub_node(parent_node=self._root2, display_value="Node 1")
            _ = self._ctl_tree.add_sub_node(parent_node=self._root2, display_value="Node 3")
            _ = self._ctl_tree.add_sub_node(parent_node=self._root2, display_value="Node 3")

        flat_list = [
            ["A1", "B1", "C1"],
            ["A1", "B1", "C2"],
            ["A1", "B2", "C3"],
            ["A2", "B3", "C4"],
            ["A2", "B3", "C5"],
            ["A2", "B3", "C6"],
            ["A2", "B4", "Razor"],
        ]
        self._ctl_tree.add_sub_tree(flat_tree=flat_list, parent_node=None)
        self._ctl_tree.add_sub_tree(flat_tree=flat_list, parent_node=self._root2)
        # tree = self._tree1.convert_to_tree(flat_list)

        self._ctl_tree.add_event_mouse_entered(self._fn_on_mouse_entered)
        self._ctl_tree.add_event_mouse_exited(self._fn_on_mouse_exit)
        self._ctl_tree.add_event_selection_changed(self._fn__on_tree_selection_changed)
        self._init_buttons()

    def _init_buttons(self) -> None:
        """Add OK, Cancel and Info buttons to dialog control"""
        self._ctl_btn_cancel = Dialogs.insert_button(
            dialog_ctrl=self._dialog.control,
            label="Cancel",
            x=self._width - self._btn_width - self._margin,
            y=self._height - self._btn_height - self._padding,
            width=self._btn_width,
            height=self._btn_height,
            btn_type=PushButtonType.CANCEL,
        )
        sz = self._ctl_btn_cancel.view.getPosSize()
        self._ctl_btn_ok = Dialogs.insert_button(
            dialog_ctrl=self._dialog.control,
            label="OK",
            x=sz.X - sz.Width - self._margin,
            y=sz.Y,
            width=self._btn_width,
            height=self._btn_height,
            btn_type=PushButtonType.OK,
            DefaultButton=True,
        )

        self._ctl_btn_info = Dialogs.insert_button(
            dialog_ctrl=self._dialog.control,
            label="Info",
            x=self._margin,
            y=sz.Y,
            width=self._btn_width,
            height=self._btn_height,
        )
        self._ctl_btn_info.view.setActionCommand("INFO")
        self._ctl_btn_info.model.HelpText = "Show info for selected items."
        self._ctl_btn_info.add_event_action_performed(self._fn_button_action_preformed)

    # region search
    def _search(self) -> None:
        se = SearchTree("C5", match_all=True)
        se.match_all = False
        se.register_rule(RuleDataInsensitive())
        se.register_rule(RuleTextInsensitive())
        # se.register_rule(RuleDataSensitive)
        result = se.find_node(self._root2)
        if result:
            print("Search Result:", result.getDisplayValue())
        else:
            print("Search Value, Not found")

        se = SearchTree("")
        se.register_rule(RuleTextRegex("R.zor"))

        result = se.find_node(self._root2)
        if result:
            print("Search Result:", result.getDisplayValue())
        else:
            print("Search Value, Not found")

    # endregion search

    # region Event Handlers
    def _init_handlers(self) -> None:
        self._fn_on_mouse_entered = self.on_mouse_entered
        self._fn_on_mouse_exit = self.on_mouse_exit
        self._fn__on_tree_selection_changed = self.on_tree_selection_changed
        self._fn_button_action_preformed = self.on_button_action_preformed

    def on_mouse_entered(self, src: Any, event: EventArgs, control_src: CtlTree, *args, **kwargs) -> None:
        # print(control_src)
        print("Mouse Entered:", control_src.name)

    def on_mouse_exit(self, src: Any, event: EventArgs, control_src: CtlTree, *args, **kwargs) -> None:
        # print(control_src)
        print("Mouse Exited:", control_src.name)

    def on_tree_selection_changed(self, src: Any, event: EventArgs, control_src: CtlTree, *args, **kwargs) -> None:
        # print(control_src)
        print("Selection changed:", control_src.name)

    def on_button_action_preformed(self, src: Any, event: EventArgs, control_src: Any, *args, **kwargs) -> None:
        """Method that is fired when Info button is clicked."""
        itm_event = cast("ActionEvent", event.event_data)
        if itm_event.ActionCommand == "INFO":
            node = self._ctl_tree.current_selection
            if node:
                _ = MsgBox.msgbox(
                    title="Info",
                    msg=f"Selected node: {node.getDisplayValue()}",
                    boxtype=MessageBoxType.INFOBOX,
                    buttons=MessageBoxResultsEnum.OK,
                )
            else:
                _ = MsgBox.msgbox(
                    title="Info",
                    msg="No node selected.",
                    boxtype=MessageBoxType.INFOBOX,
                    buttons=MessageBoxResultsEnum.OK,
                )

    # endregion Event Handlers

    def show(self) -> None:
        window = mLo.Lo.get_frame().getContainerWindow()
        ps = window.getPosSize()
        x = round(ps.Width / 2 - self._width / 2)
        y = round(ps.Height / 2 - self._height / 2)
        self._dialog.setTitle(self._title)
        self._dialog.setPosSize(x, y, self._width, self._height, PosSize.POSSIZE)
        self._dialog.setVisible(True)
        self._search()
        self._dialog.execute()
        self._dialog.dispose()


def main():
    with mLo.Lo.Loader(mLo.Lo.ConnectSocket(), opt=mLo.Lo.Options(verbose=True)):
        doc = Calc.create_doc()
        GUI.set_visible(visible=True, doc=doc)
        run()


def run() -> None:
    inst = Tree()
    inst.show()


if __name__ == "__main__":
    main()
