from __future__ import annotations
from typing import Any, cast, List, overload, Sequence, TYPE_CHECKING
import uno

from com.sun.star.beans import XPropertySet
from com.sun.star.frame import XModel
from com.sun.star.style import XStyle
from com.sun.star.text import XTextFramesSupplier
from ooo.dyn.style.numbering_type import NumberingTypeEnum
from ooo.dyn.text.page_number_type import PageNumberType

from ooodev.adapter.beans.property_change_implement import PropertyChangeImplement
from ooodev.adapter.beans.vetoable_change_implement import VetoableChangeImplement
from ooodev.adapter.container.name_access_comp import NameAccessComp
from ooodev.adapter.document.document_event_events import DocumentEventEvents
from ooodev.adapter.text.text_document_comp import TextDocumentComp
from ooodev.adapter.text.textfield.page_count_comp import PageCountComp
from ooodev.adapter.text.textfield.page_number_comp import PageNumberComp
from ooodev.adapter.util.modify_events import ModifyEvents
from ooodev.adapter.util.refresh_events import RefreshEvents
from ooodev.adapter.view.print_job_events import PrintJobEvents
from ooodev.dialog.partial.create_dialog_partial import CreateDialogPartial
from ooodev.events.args.cancel_event_args import CancelEventArgs
from ooodev.events.args.event_args import EventArgs
from ooodev.events.args.listener_event_args import ListenerEventArgs
from ooodev.events.partial.events_partial import EventsPartial
from ooodev.events.write_named_event import WriteNamedEvent
from ooodev.exceptions import ex as mEx
from ooodev.format.inner.style_partial import StylePartial
from ooodev.format.writer.style import FamilyNamesKind
from ooodev.format.writer.style.char.kind.style_char_kind import StyleCharKind
from ooodev.format.writer.style.frame.style_frame_kind import StyleFrameKind
from ooodev.format.writer.style.lst.style_list_kind import StyleListKind
from ooodev.format.writer.style.page.kind.writer_style_page_kind import WriterStylePageKind
from ooodev.format.writer.style.para.kind.style_para_kind import StyleParaKind
from ooodev.office import write as mWrite
from ooodev.utils import gui as mGUI
from ooodev.utils import info as mInfo
from ooodev.loader import lo as mLo
from ooodev.utils import selection as mSelection
from ooodev.utils.context.lo_context import LoContext
from ooodev.utils.partial.dispatch_partial import DispatchPartial
from ooodev.utils.data_type.size import Size
from ooodev.loader.inst import DocType

from ooodev.loader.inst import Service as LoService
from ooodev.utils.kind.zoom_kind import ZoomKind
from ooodev.utils.partial.doc_io_partial import DocIoPartial
from ooodev.utils.partial.gui_partial import GuiPartial
from ooodev.utils.partial.lo_inst_props_partial import LoInstPropsPartial
from ooodev.utils.partial.prop_partial import PropPartial
from ooodev.utils.partial.qi_partial import QiPartial
from ooodev.utils.partial.service_partial import ServicePartial

# from . import write_draw_page as mWriteDrawPage
from . import write_paragraph_cursor as mWriteParagraphCursorCursor
from . import write_paragraphs as mWriteParagraphs
from . import write_sentence_cursor as mWriteSentenceCursor
from . import write_text as mWriteText
from . import write_text_content as mWriteTextContent
from . import write_text_cursor as mWriteTextCursor
from . import write_text_range as mWriteTextRange
from . import write_text_view_cursor as mWriteTextViewCursor
from . import write_word_cursor as mWriteWordCursor
from .style import write_cell_style as mWriteCellStyle
from .style import write_character_style as mWriteCharacterStyle
from .style import write_numbering_style as mWriteNumberingStyle
from .style import write_page_style as mWritePageStyle
from .style import write_paragraph_style as mWriteParagraphStyle
from .style import write_style as mWriteStyle
from .style import write_style_families as mWriteStyleFamilies
from .write_draw_page import WriteDrawPage
from .write_draw_pages import WriteDrawPages
from .write_text_frames import WriteTextFrames

if TYPE_CHECKING:
    from com.sun.star.frame import XController
    from com.sun.star.graphic import XGraphic
    from com.sun.star.text import XText
    from com.sun.star.text import XTextDocument
    from com.sun.star.text import XTextRange
    from ooo.dyn.view.paper_format import PaperFormat
    from ooodev.proto.style_obj import StyleT
    from ooodev.loader.inst import LoInst


class WriteDoc(
    LoInstPropsPartial,
    TextDocumentComp,
    DocumentEventEvents,
    ModifyEvents,
    PrintJobEvents,
    RefreshEvents,
    PropertyChangeImplement,
    VetoableChangeImplement,
    QiPartial,
    PropPartial,
    GuiPartial,
    ServicePartial,
    EventsPartial,
    StylePartial,
    DocIoPartial["WriteDoc"],
    CreateDialogPartial,
    DispatchPartial,
):
    """A class to represent a Write document."""

    DOC_TYPE: DocType = DocType.WRITER

    def __init__(self, doc: XTextDocument, lo_inst: LoInst | None = None) -> None:
        """
        Constructor

        Args:
            doc (XTextDocument): A UNO object that supports ``com.sun.star.text.TextDocument`` service.
            lo_inst (LoInst, optional): Lo instance. Used when creating multiple documents. Defaults to ``None``.

        Raises:
            NotSupportedDocumentError: If document is not a Writer document.

        Returns:
            None:
        """
        if lo_inst is None:
            lo_inst = mLo.Lo.current_lo

        if not mInfo.Info.is_doc_type(doc, LoService.WRITER):
            raise mEx.NotSupportedDocumentError("Document is not a Writer document")

        LoInstPropsPartial.__init__(self, lo_inst=lo_inst)

        TextDocumentComp.__init__(self, doc)  # type: ignore
        generic_args = self._ComponentBase__get_generic_args()  # type: ignore
        DocumentEventEvents.__init__(self, trigger_args=generic_args, cb=self._on_document_event_add_remove)
        ModifyEvents.__init__(self, trigger_args=generic_args, cb=self._on_modify_events_add_remove)
        PrintJobEvents.__init__(self, trigger_args=generic_args, cb=self._on_print_job_add_remove)
        RefreshEvents.__init__(self, trigger_args=generic_args, cb=self._on_refresh_add_remove)
        PropertyChangeImplement.__init__(self, component=self.component, trigger_args=generic_args)
        VetoableChangeImplement.__init__(self, component=self.component, trigger_args=generic_args)
        QiPartial.__init__(self, component=doc, lo_inst=self.lo_inst)
        PropPartial.__init__(self, component=doc, lo_inst=self.lo_inst)
        GuiPartial.__init__(self, component=doc, lo_inst=self.lo_inst)
        ServicePartial.__init__(self, component=doc, lo_inst=self.lo_inst)
        EventsPartial.__init__(self)
        StylePartial.__init__(self, component=doc)
        DocIoPartial.__init__(self, owner=self, lo_inst=self.lo_inst)
        CreateDialogPartial.__init__(self, lo_inst=self.lo_inst)
        DispatchPartial.__init__(self, lo_inst=self.lo_inst, events=self)
        self._draw_page = None
        self._draw_pages = None
        self._text_frames = None

    # region Lazy Listeners

    def _on_modify_events_add_remove(self, source: Any, event: ListenerEventArgs) -> None:
        # will only ever fire once
        self.component.addModifyListener(self.events_listener_modify)
        event.remove_callback = True

    def _on_document_event_add_remove(self, source: Any, event: ListenerEventArgs) -> None:
        # will only ever fire once
        self.component.addDocumentEventListener(self.events_listener_document_event)
        event.remove_callback = True

    def _on_print_job_add_remove(self, source: Any, event: ListenerEventArgs) -> None:
        # will only ever fire once
        self.component.addPrintJobListener(self.events_listener_print_job)
        event.remove_callback = True

    def _on_refresh_add_remove(self, source: Any, event: ListenerEventArgs) -> None:
        # will only ever fire once
        self.component.addRefreshListener(self.events_listener_refresh)
        event.remove_callback = True

    # endregion Lazy Listeners

    def get_controller(self) -> XController:
        """
        Gets controller from document.

        Returns:
            XController: Controller.
        """
        model = self.qi(XModel, True)
        return model.getCurrentController()

    # region get_cursor()
    @overload
    def get_cursor(self) -> mWriteTextCursor.WriteTextCursor[WriteDoc]:
        """
        Gets text cursor from the current document.

        Returns:
            WriteTextCursor: Cursor
        """
        ...

    @overload
    def get_cursor(self, *, cursor_obj: Any) -> mWriteTextCursor.WriteTextCursor[WriteDoc]:
        """
        Gets text cursor

        Args:
            cursor_obj (Any): Text Document or Text Cursor

        Returns:
            WriteTextCursor: Cursor
        """
        ...

    @overload
    def get_cursor(self, *, rng: XTextRange, txt: XText) -> mWriteTextCursor.WriteTextCursor[WriteDoc]:
        """
        Gets text cursor

        Args:
            rng (XTextRange): Text Range Instance
            txt (XText): Text Instance

        Returns:
            WriteTextCursor: Cursor
        """
        ...

    @overload
    def get_cursor(self, *, rng: XTextRange) -> mWriteTextCursor.WriteTextCursor[WriteDoc]:
        """
        Gets text cursor

        Args:
            rng (XTextRange): Text Range instance

        Returns:
            WriteTextCursor: Cursor
        """
        ...

    def get_cursor(self, **kwargs) -> mWriteTextCursor.WriteTextCursor[WriteDoc]:
        """Returns the cursor of the document."""
        if not kwargs:
            return mWriteTextCursor.WriteTextCursor(
                owner=self, component=self.component.getText().createTextCursor(), lo_inst=self.lo_inst
            )
        if "text_doc" in kwargs:
            kwargs["text_doc"] = self.component
        with LoContext(self.lo_inst):
            result = mWrite.Write.get_cursor(**kwargs)
        return mWriteTextCursor.WriteTextCursor(owner=self, component=result, lo_inst=self.lo_inst)

    # endregion get_cursor()

    # region DocIoPartial overrides
    def _on_io_saving(self, event_args: CancelEventArgs) -> None:
        """
        Event called before document is saved.

        Args:
            event_args (CancelEventArgs): Event data.

        Raises:
            CancelEventError: If event is canceled.
        """
        event_args.event_data["text_doc"] = self.component
        self.trigger_event(WriteNamedEvent.DOC_SAVING, event_args)

    def _on_io_saved(self, event_args: EventArgs) -> None:
        """
        Event called after document is saved.

        Args:
            event_args (EventArgs): Event data.
        """
        self.trigger_event(WriteNamedEvent.DOC_SAVED, event_args)

    def _on_io_closing(self, event_args: CancelEventArgs) -> None:
        """
        Event called before document is closed.

        Args:
            event_args (CancelEventArgs): Event data.

        Raises:
            CancelEventError: If event is canceled.
        """
        event_args.event_data["text_doc"] = self.component
        self.trigger_event(WriteNamedEvent.DOC_CLOSING, event_args)

    def _on_io_closed(self, event_args: EventArgs) -> None:
        """
        Event called after document is closed.

        Args:
            event_args (EventArgs): Event data.
        """
        self.trigger_event(WriteNamedEvent.DOC_CLOSED, event_args)

    # region from_current_doc()
    @classmethod
    def _on_from_current_doc_loaded(cls, event_args: EventArgs) -> None:
        """
        Event called after from_current_doc is called.

        Args:
            event_args (EventArgs): Event data.

        Returns:
            None:

        Note:
            event_args.event_data is a dictionary and contains the document in a key named 'doc'.
        """
        doc = cast(WriteDoc, event_args.event_data["doc"])
        if doc.DOC_TYPE != DocType.WRITER:
            raise mEx.NotSupportedDocumentError(f"Document '{type(doc).__name__}' is not a Write document.")

    # endregion from_current_doc()

    # endregion DocIoPartial overrides

    # region Close Document

    def close_doc(self, deliver_ownership=True) -> bool:
        """
        Closes text document

        Args:
            deliver_ownership (bool, optional): If ``True`` ownership is delivered to caller. Default ``True``.
                ``True`` delegates the ownership of this closing object to anyone which throw the CloseVetoException.
                This new owner has to close the closing object again if his still running processes will be finished.
                ``False`` let the ownership at the original one which called the close() method.
                They must react for possible CloseVetoExceptions such as when document needs saving and
                try it again at a later time. This can be useful for a generic UI handling.

        Returns:
            bool: ``False`` if ``DOC_CLOSING`` event is canceled, Otherwise ``True``.

        :events:
            .. cssclass:: lo_event

                - :py:attr:`~.events.write_named_event.WriteNamedEvent.DOC_CLOSING` :eventref:`src-docs-event-cancel`
                - :py:attr:`~.events.write_named_event.WriteNamedEvent.DOC_CLOSED` :eventref:`src-docs-event`

        Note:
            Event args ``event_data`` is a dictionary containing ``text_doc``.

        Attention:
            :py:meth:`Lo.close <.utils.lo.Lo.close>` method is called along with any of its events.
        """

        return self.close(deliver_ownership)

    # endregion Close Document

    def compare_cursor_ends(self, c1: XTextRange, c2: XTextRange) -> mSelection.Selection.CompareEnum:
        """
        Compares two cursors ranges end positions

        Args:
            c1 (XTextRange): first cursor range
            c2 (XTextRange): second cursor range

        Raises:
            Exception: if comparison fails

        Returns:
            CompareEnum: Compare result.
            :py:attr:`.CompareEnum.BEFORE` if ``c1`` end position is before ``c2`` end position.
            :py:attr:`.CompareEnum.EQUAL` if ``c1`` end position is equal to ``c2`` end position.
            :py:attr:`.CompareEnum.AFTER` if ``c1`` end position is after ``c2`` end position.
        """
        with LoContext(self.lo_inst):
            result = mSelection.Selection.compare_cursor_ends(c1, c2)
        return result

    def create_style_char(
        self, style_name: str, styles: Sequence[StyleT] | None = None
    ) -> mWriteCharacterStyle.WriteCharacterStyle:
        """
        Creates a character style and adds it to document character styles.

        Args:
            text_doc (XTextDocument): Text Document
            style_name (str): The name of the character style.
            styles (Sequence[StyleT], optional): One or more styles to apply.

        Returns:
            WriteCharacterStyle: Newly created style
        """
        if styles is None:
            styles = ()
        with LoContext(self.lo_inst):
            result = mWrite.Write.create_style_char(self.component, style_name, styles)
        return mWriteCharacterStyle.WriteCharacterStyle(owner=self, component=result, lo_inst=self.lo_inst)

    def create_style_para(
        self, style_name: str, styles: Sequence[StyleT] | None = None
    ) -> mWriteParagraphStyle.WriteParagraphStyle[WriteDoc]:
        """
        Creates a paragraph style and adds it to document paragraph styles.

        Args:
            style_name (str): The name of the paragraph style.
            styles (Sequence[StyleT], optional): One or more styles to apply.

        Returns:
            WriteParagraphStyle: Newly created style
        """
        if styles is None:
            styles = ()
        with LoContext(self.lo_inst):
            result = mWrite.Write.create_style_para(self.component, style_name, styles)
        return mWriteParagraphStyle.WriteParagraphStyle(owner=self, component=result, lo_inst=self.lo_inst)

    def find_bookmark(self, bm_name: str) -> mWriteTextContent.WriteTextContent[WriteDoc] | None:
        """
        Finds a bookmark

        Args:
            bm_name (str): Bookmark name

        Returns:
            WriteTextContent | None: Bookmark if found; Otherwise, None
        """
        result = mWrite.Write.find_bookmark(self.component, bm_name)
        if result is None:
            return None
        return mWriteTextContent.WriteTextContent(owner=self, component=result, lo_inst=self.lo_inst)

    def get_view_cursor(self) -> mWriteTextViewCursor.WriteTextViewCursor[WriteDoc]:
        """
        Gets document view cursor.

        Describes a cursor in a text document's view.

        Raises:
            ViewCursorError: If Unable to get cursor

        Returns:
            WriteTextViewCursor: Text View Cursor

        See Also:
            `LibreOffice API XTextViewCursor <https://api.libreoffice.org/docs/idl/ref/interfacecom_1_1sun_1_1star_1_1text_1_1XTextViewCursor.html>`_
        """
        cursor = mSelection.Selection.get_view_cursor(self.component)
        return mWriteTextViewCursor.WriteTextViewCursor(owner=self, component=cursor, lo_inst=self.lo_inst)

    def get_doc_path(self) -> str:
        """
        Gets document path as a System path such has ``C:\\Users\\User\\Documents\\MyDoc.odt``.

        Returns:
            PathOrStr: Document path if available; Otherwise empty string.

        .. versionadded:: 0.20.4
        """
        try:
            return uno.fileUrlToSystemPath(self.component.URL)  # type: ignore
        except Exception:
            return ""

    def get_doc_settings(self) -> XPropertySet:
        """
        Gets Text Document Settings

        Returns:
            XPropertySet: Settings

        See Also:
            `API DocumentSettings Service <https://api.libreoffice.org/docs/idl/ref/servicecom_1_1sun_1_1star_1_1text_1_1DocumentSettings.html>`__
        """
        return self.lo_inst.create_instance_msf(XPropertySet, "com.sun.star.text.DocumentSettings", raise_err=True)

    def get_graphic_links(self) -> NameAccessComp | None:
        """
        Gets graphic links

        Args:
            doc (XComponent): Document

        Raises:
            MissingInterfaceError: if doc does not implement ``XTextGraphicObjectsSupplier`` interface

        Returns:
            NameAccessComp | None: Graphic Links on success, Otherwise, None
        """
        result = mWrite.Write.get_graphic_links(self.component)
        if result is None:
            return None
        return NameAccessComp(result)

    def get_left_cursor(self, rng: XTextRange) -> mWriteTextCursor.WriteTextCursor[WriteDoc]:
        """
        Creates a new TextCursor with position left that can travel right.

        Args:
            rng (XTextRange): Text Range.

        Returns:
            WriteTextCursor: a new instance of a TextCursor which is located at the specified
            TextRange to travel in the given text context.
        """
        with LoContext(self.lo_inst):
            result = mSelection.Selection.get_left_cursor(rng, self.component)
        return mWriteTextCursor.WriteTextCursor(owner=self, component=result, lo_inst=self.lo_inst)

    def get_num_of_pages(self) -> int:
        """
        Gets document page count

        Returns:
            int: page count
        """
        result = mWrite.Write.get_num_of_pages(self.component)
        return result

    def get_page_count_field(self, numbering_type: NumberingTypeEnum = NumberingTypeEnum.ARABIC) -> PageCountComp:
        """
        Gets page count field

        Returns:
            PageCountComp: Page Count Field
        """
        with LoContext(self.lo_inst):
            result = mWrite.Write.get_page_count(numbering_type=numbering_type)
        return PageCountComp(result)

    def get_page_number_field(
        self,
        numbering_type: NumberingTypeEnum = NumberingTypeEnum.ARABIC,
        sub_type: PageNumberType = PageNumberType.CURRENT,
    ) -> PageNumberComp:
        """
        Gets Arabic style number showing current page value

        Args:
            numbering_type (NumberingTypeEnum, optional): Numbering Type. Defaults to ``NumberingTypeEnum.ARABIC``.
            sub_type (PageNumberType, optional): Page Number Type. Defaults to ``PageNumberType.CURRENT``.

        Returns:
            PageNumberComp: Page Number Field
        """
        with LoContext(self.lo_inst):
            result = mWrite.Write.get_page_number(numbering_type=numbering_type, sub_type=sub_type)
        return PageNumberComp(result)

    def get_page_size(self) -> Size:
        """
        Get page size in ``1/100 mm`` units.

        Raises:
            PropertiesError: If unable to access properties
            Exception: If unable to get page size

        Returns:
            ~ooodev.utils.data_type.size.Size: Page Size in ``1/100 mm`` units.
        """
        return mWrite.Write.get_page_size(self.component)

    def get_page_text_size(self) -> Size:
        """
        Get page text size in ``1/100 mm`` units.

        Raises:
            PropertiesError: If unable to access properties
            Exception: If unable to get page size

        Returns:
            ~ooodev.utils.data_type.size.Size: Page text Size in ``1/100 mm`` units.
        """
        return mWrite.Write.get_page_text_size(self.component)

    def get_page_text_width(self) -> int:
        """
        Get the width of the page's text area in ``1/100 mm`` units.

        Returns:
            int: Page Width in ``1/100 mm`` units on success; Otherwise 0
        """
        return mWrite.Write.get_page_text_width(self.component)

    def get_selected(self) -> mWriteTextRange.WriteTextRange[WriteDoc] | None:
        """
        Gets the text range for current selection

        Args:
            text_doc (XTextDocument): Text Document

        Raises:
            MissingInterfaceError: If unable to obtain required interface.

        Returns:
            WriteTextRange | None: If no selection is made then None is returned; Otherwise, Text Range.

        Note:
            Writer must be visible for this method or ``None`` is returned.
        """
        result = mSelection.Selection.get_selected_text_range(self.component)
        if result is None:
            return None
        return mWriteTextRange.WriteTextRange(owner=self, component=result, lo_inst=self.lo_inst)

    def get_selected_str(self) -> str:
        """
        Gets the first selection text for Document

        Returns:
            str: Selected text or empty string.

        Note:
            Writer must be visible for this method or empty string is returned.
        """
        return mSelection.Selection.get_selected_text_str(self.component)

    def get_draw_page(self) -> WriteDrawPage[WriteDoc]:
        """
        Gets draw page.

        Returns:
            GenericDrawPage: Draw Page
        """
        return self.draw_page

    def get_draw_pages(self) -> WriteDrawPages:
        """
        Gets draw pages.

        Returns:
            GenericDrawPages: Draw Page
        """
        return self.draw_pages

    def get_paragraph_cursor(self) -> mWriteParagraphCursorCursor.WriteParagraphCursor:
        """
        Gets document paragraph cursor

        Raises:
            ParagraphCursorError: If Unable to get cursor

        Returns:
            WriteParagraphCursor: Paragraph cursor
        """
        result = mSelection.Selection.get_paragraph_cursor(self.component)
        return mWriteParagraphCursorCursor.WriteParagraphCursor(owner=self, component=result, lo_inst=self.lo_inst)

    def get_right_cursor(self, rng: XTextRange) -> mWriteTextCursor.WriteTextCursor[WriteDoc]:
        """
        Creates a new TextCursor with position right that can travel left.

        Args:
            rng (XTextRange): Text Range.

        Returns:
            WriteTextCursor: a new instance of a TextCursor which is located at the specified
            TextRange to travel in the given text context.
        """
        with LoContext(self.lo_inst):
            result = mSelection.Selection.get_right_cursor(rng, self.component)
        return mWriteTextCursor.WriteTextCursor(owner=self, component=result, lo_inst=self.lo_inst)

    def get_style_names(
        self, family_style_name: str | FamilyNamesKind = FamilyNamesKind.PARAGRAPH_STYLES
    ) -> List[str]:
        """
        Gets a list of style names

        Args:
            family_style_name (str, FamilyNamesKind, optional): name of family style. Default is ``FamilyNamesKind.PARAGRAPH_STYLES``.

        Raises:
            StyleError: If unable to access Style names

        Returns:
            List[str]: List of style names
        """
        try:
            return mInfo.Info.get_style_names(self.component, str(family_style_name))
        except Exception as e:
            raise mEx.StyleError("Unable to get style names") from e

    def get_style_families(self) -> mWriteStyleFamilies.WriteStyleFamilies:
        """
        Gets a cell style by name.

        Raises:
            StyleError: If unable to get style

        Returns:
            WriteStyleFamilies: Style
        """
        # there are no styles for cell by default in a writer document.
        try:
            result = mInfo.Info.get_style_families(self.component)
            return mWriteStyleFamilies.WriteStyleFamilies(owner=self, component=result, lo_inst=self.lo_inst)
        except Exception as e:
            raise mEx.StyleError("Unable to get style families") from e

    def get_style_cell(self, name: str = "Standard") -> mWriteCellStyle.WriteCellStyle[WriteDoc]:
        """
        Gets a cell style by name.

        Args:
            name (str, optional): Name of style to get. Defaults to ``Standard``.

        Raises:
            StyleError: If unable to get style

        Returns:
            WriteCellStyle: Style
        """
        # there are no styles for cell by default in a writer document.
        try:
            result = mInfo.Info.get_style_props(self.component, "CellStyles", str(name))
            return mWriteCellStyle.WriteCellStyle(
                owner=self, component=mLo.Lo.qi(XStyle, result, True), lo_inst=self.lo_inst
            )
        except Exception as e:
            raise mEx.StyleError(f"Unable to get style: {name}") from e

    def get_style_character(
        self, name: str | StyleCharKind = "Standard"
    ) -> mWriteCharacterStyle.WriteCharacterStyle[WriteDoc]:
        """
        Gets a character style by name.

        Args:
            name (str, StyleCharKind, optional): Name of style to get. Defaults to ``Standard``.

        Raises:
            StyleError: If unable to get style

        Returns:
            WriteCharacterStyle: Style
        """
        try:
            result = mInfo.Info.get_style_props(self.component, "CharacterStyles", str(name))
            return mWriteCharacterStyle.WriteCharacterStyle(
                owner=self, component=mLo.Lo.qi(XStyle, result, True), lo_inst=self.lo_inst
            )
        except Exception as e:
            raise mEx.StyleError(f"Unable to get style: {name}") from e

    def get_style_frame(self, name: str | StyleFrameKind = "Frame") -> mWriteStyle.WriteStyle[WriteDoc]:
        """
        Gets a frame style by name.

        Args:
            name (str, StyleFrameKind, optional): Name of style to get. Defaults to ``Frame``.

        Raises:
            StyleError: If unable to get style

        Returns:
            WriteStyle: Style
        """
        try:
            result = mInfo.Info.get_style_props(self.component, "FrameStyles", str(name))
            return mWriteStyle.WriteStyle(owner=self, component=mLo.Lo.qi(XStyle, result, True), lo_inst=self.lo_inst)
        except Exception as e:
            raise mEx.StyleError(f"Unable to get style: {name}") from e

    def get_style_numbering(
        self, name: str | StyleListKind = StyleListKind.NUM_123
    ) -> mWriteNumberingStyle.WriteNumberingStyle[WriteDoc]:
        """
        Gets a character style by name.

        Args:
            name (str, StyleListKind, optional): Name of style to get. Defaults to ``StyleListKind.NUM_123``.

        Raises:
            StyleError: If unable to get style

        Returns:
            WriteNumberingStyle: Style
        """
        try:
            result = mInfo.Info.get_style_props(self.component, "NumberingStyles", str(name))
            return mWriteNumberingStyle.WriteNumberingStyle(
                owner=self, component=mLo.Lo.qi(XStyle, result, True), lo_inst=self.lo_inst
            )
        except Exception as e:
            raise mEx.StyleError(f"Unable to get style: {name}") from e

    def get_style_paragraph(
        self, name: str | StyleParaKind = "Standard"
    ) -> mWriteParagraphStyle.WriteParagraphStyle[WriteDoc]:
        """
        Gets a paragraph style by name.

        Args:
            name (str, StyleParaKind, optional): Name of style to get. Defaults to ``Standard``.

        Raises:
            StyleError: If unable to get style

        Returns:
            WriteParagraphStyle: Style
        """
        try:
            result = mInfo.Info.get_style_props(self.component, "ParagraphStyles", str(name))
            return mWriteParagraphStyle.WriteParagraphStyle(
                owner=self, component=mLo.Lo.qi(XStyle, result, True), lo_inst=self.lo_inst
            )
        except Exception as e:
            raise mEx.StyleError(f"Unable to get style: {name}") from e

    def get_style_page(self, name: str | WriterStylePageKind = "Standard") -> mWritePageStyle.WritePageStyle[WriteDoc]:
        """
        Gets a page style by name.

        Args:
            name (str, WriterStylePageKind, optional): Name of style to get. Defaults to ``Standard``.

        Raises:
            StyleError: If unable to get style

        Returns:
            WritePageStyle: Style
        """
        try:
            result = mInfo.Info.get_style_props(self.component, "PageStyles", str(name))
            return mWritePageStyle.WritePageStyle(
                owner=self, component=mLo.Lo.qi(XStyle, result, True), lo_inst=self.lo_inst
            )
        except Exception as e:
            raise mEx.StyleError(f"Unable to get style: {name}") from e

    def get_style_table(self, name: str = "Default Style") -> mWriteStyle.WriteStyle[WriteDoc]:
        """
        Gets a table style by name.

        Args:
            name (str, optional): Name of style to get. Defaults to ``Default Style``.

        Raises:
            StyleError: If unable to get style

        Returns:
            WriteStyle: Style
        """
        try:
            result = mInfo.Info.get_style_props(self.component, "TableStyles", str(name))
            return mWriteStyle.WriteStyle(owner=self, component=mLo.Lo.qi(XStyle, result, True), lo_inst=self.lo_inst)
        except Exception as e:
            raise mEx.StyleError(f"Unable to get style: {name}") from e

    def get_text(self) -> mWriteText.WriteText[WriteDoc]:
        """
        Gets text that is enumerable.

        Returns:
            WriteText: Text.
        """
        return mWriteText.WriteText(owner=self, component=self.component.getText(), lo_inst=self.lo_inst)

    def get_text_paragraphs(self) -> mWriteParagraphs.WriteParagraphs[WriteDoc]:
        """
        Gets text that is enumerable.

        Returns:
            WriteText: Text.
        """
        return mWriteParagraphs.WriteParagraphs(owner=self, component=self.component.getText(), lo_inst=self.lo_inst)

    def get_text_frames(self) -> WriteTextFrames:
        """
        Gets document Text Frames.

        Args:
            doc (XComponent): Document.

        Returns:
            WriteTextFrames: Document Text Frames
        """
        # result = mWrite.Write.get_text_frames(self.component)
        # if result is None:
        #     return None
        # return NameAccessComp(result)
        return self.text_frames

    def get_sentence_cursor(self) -> mWriteSentenceCursor.WriteSentenceCursor:
        """
        Gets document sentence cursor.

        Raises:
            SentenceCursorError: If Unable to get cursor.

        Returns:
            WriteSentenceCursor: Sentence Cursor.
        """
        result = mSelection.Selection.get_sentence_cursor(self.component)
        return mWriteSentenceCursor.WriteSentenceCursor(owner=self, component=result, lo_inst=self.lo_inst)

    def get_text_graphics(self) -> List[XGraphic]:
        """
        Gets text graphics.

        Raises:
            Exception: If unable to get text graphics

        Returns:
            List[XGraphic]: Text Graphics

        Note:
            If there is error getting a graphic link then it is ignored
            and not added to the return value.
        """
        return mWrite.Write.get_text_graphics(self.component)

    def get_word_cursor(self) -> mWriteWordCursor.WriteWordCursor:
        """
        Gets document word cursor.


        Raises:
            WordCursorError: If Unable to get cursor.

        Returns:
            WriteWordCursor: Word Cursor.
        """
        result = mSelection.Selection.get_word_cursor(self.component)
        return mWriteWordCursor.WriteWordCursor(owner=self, component=result, lo_inst=self.lo_inst)

    def is_anything_selected(self) -> bool:
        """
        Determine if anything is selected.

        If Write document is not visible this method returns false.

        Returns:
            bool: True if anything in the document is selected: Otherwise, False

        Note:
            Writer must be visible for this method or ``False`` is always returned.
        """
        return mSelection.Selection.is_anything_selected(self.component)

    def select_next_word(self) -> bool:
        """
        Select the word right from the current cursor position.

        Returns:
            bool: True if go to next word succeeds; Otherwise, False.

        :events:
            .. cssclass:: lo_event

                - :py:attr:`~.events.write_named_event.WriteNamedEvent.WORD_SELECTING` :eventref:`write_word_selecting`
                - :py:attr:`~.events.write_named_event.WriteNamedEvent.WORD_SELECTED` :eventref:`write_word_selected`

        Note:
            The method returning ``True`` does not necessarily mean that the cursor is located at
            the next word, or any word at all! This may happen for example if it travels over empty paragraphs.

        Note:
            Event args ``event_data`` is a dictionary containing ``text_doc``.
        """
        return mSelection.Selection.select_next_word(self.component)

    def set_a4_page_format(
        self,
    ) -> bool:
        """
        Set Page Format to A4

        Returns:
            bool: ``True`` if page format is set; Otherwise, ``False``

        See Also:
            :py:meth:`~.WriteDoc.set_page_format`

        Attention:
            :py:meth:`~.write.Write.set_page_format` method is called along with any of its events.
        """
        return mWrite.Write.set_a4_page_format(self.component)

    def set_footer(self, text: str, styles: Sequence[StyleT] | None = None) -> None:
        """
        Modify the footer via the page style for the document.
        Put the text on the right hand side in the header in
        a general font of 10pt.

        Args:
            text (str): Header Text
            styles (Sequence[StyleT]): Styles to apply to the text.

        Raises:
            PropertiesError: If unable to access properties
            Exception: If unable to set header text

        See Also:
            :py:meth:`~.WriteDoc.set_header`

        Note:
            The font applied is determined by :py:meth:`.Info.get_font_general_name`
        """
        mWrite.Write.set_footer(self.component, text, styles)

    def set_header(self, text: str, styles: Sequence[StyleT] | None = None) -> None:
        """
        Modify the header via the page style for the document.
        Put the text on the right hand side in the header in
        a general font of 10pt.

        Args:
            text (str): Header Text
            styles (Sequence[StyleT]): Styles to apply to the text.

        Raises:
            PropertiesError: If unable to access properties
            Exception: If unable to set header text

        See Also:
            :py:meth:`~.WriteDoc.set_footer`

        Note:
            The font applied is determined by :py:meth:`.Info.get_font_general_name`
        """
        mWrite.Write.set_header(self.component, text, styles)

    def set_page_format(self, paper_format: PaperFormat) -> bool:
        """
        Set Page Format

        Args:
            paper_format (~com.sun.star.view.PaperFormat): Paper Format.

        Raises:
            MissingInterfaceError: If ``text_doc`` does not implement ``XPrintable`` interface

        Returns:
            bool: ``True`` if page format is set; Otherwise, ``False``

        :events:
            .. cssclass:: lo_event

                - :py:attr:`~.events.write_named_event.WriteNamedEvent.PAGE_FORMAT_SETTING` :eventref:`src-docs-event-cancel`
                - :py:attr:`~.events.write_named_event.WriteNamedEvent.PAGE_FORMAT_SET` :eventref:`src-docs-event`

        Note:
            Event args ``event_data`` is a dictionary containing ``fnm``.

        See Also:
            - :py:meth:`~.write_doc.WriteDoc.set_a4_page_format`
        """
        return mWrite.Write.set_page_format(self.component, paper_format)

    def set_page_numbers(self) -> PageNumberComp:
        """
        Modify the footer via the page style for the document.
        Put page number & count in the center of the footer in Times New Roman, 12pt

        Raises:
            PropertiesError: If unable to get properties
            Exception: If Unable to set page numbers

        Returns:
            PageNumberComp: Page Number Field
        """
        with LoContext(self.lo_inst):
            result = mWrite.Write.set_page_numbers(self.component)
        return PageNumberComp(result)

    def set_visible(self, visible: bool = True) -> None:
        """
        Set window visibility.

        Args:
            visible (bool, optional): If ``True`` window is set visible; Otherwise, window is set invisible. Default ``True``

        Returns:
            None:
        """
        mGUI.GUI.set_visible(doc=self.component, visible=visible)

    def zoom(self, type: ZoomKind = ZoomKind.ENTIRE_PAGE) -> None:
        """
        Zooms document to a specific view.

        Args:
            type (ZoomKind, optional): Type of Zoom to set. Defaults to ``ZoomKind.ZOOM_100_PERCENT``.
        """

        def zoom_val(value: int) -> None:
            with LoContext(self.lo_inst):
                mGUI.GUI.zoom(view=ZoomKind.BY_VALUE, value=value)

        if type in (
            ZoomKind.ENTIRE_PAGE,
            ZoomKind.OPTIMAL,
            ZoomKind.PAGE_WIDTH,
            ZoomKind.PAGE_WIDTH_EXACT,
        ):
            with LoContext(self.lo_inst):
                mGUI.GUI.zoom(view=type)
        elif type == ZoomKind.ZOOM_200_PERCENT:
            zoom_val(200)
        elif type == ZoomKind.ZOOM_150_PERCENT:
            zoom_val(150)
        elif type == ZoomKind.ZOOM_100_PERCENT:
            zoom_val(100)
        elif type == ZoomKind.ZOOM_75_PERCENT:
            zoom_val(75)
        elif type == ZoomKind.ZOOM_50_PERCENT:
            zoom_val(50)

    def zoom_value(self, value: int = 100) -> None:
        """
        Sets the zoom level of the Document

        Args:
            value (int, optional): Value to set zoom. e.g. 160 set zoom to 160%. Default ``100``.
        """
        with LoContext(self.lo_inst):
            mGUI.GUI.zoom_value(value=value)

    # region Properties
    @property
    def draw_page(self) -> WriteDrawPage[WriteDoc]:
        """
        Gets draw page.

        Returns:
            GenericDrawPage: Draw Page
        """
        if self._draw_page is None:
            draw_page = mWrite.Write.get_draw_page(self.component)
            self._draw_page = WriteDrawPage(owner=self, component=draw_page, lo_inst=self.lo_inst)
        return self._draw_page  # type: ignore

    @property
    def draw_pages(self) -> WriteDrawPages:
        """
        Gets draw pages.

        Returns:
            GenericDrawPages: Draw Pages
        """
        if self._draw_pages is None:
            draw_pages = mWrite.Write.get_draw_pages(self.component)
            self._draw_pages = WriteDrawPages(owner=self, slides=draw_pages, lo_inst=self.lo_inst)
        return self._draw_pages  # type: ignore

    @property
    def text_frames(self) -> WriteTextFrames:
        """
        Gets text frames.

        Returns:
            WriteTextFrames: Text Frames
        """
        if self._text_frames is None:
            supplier = self.qi(XTextFramesSupplier, True)
            name_access = supplier.getTextFrames()
            self._text_frames = WriteTextFrames(owner=self, frames=name_access, lo_inst=self.lo_inst)
        return self._text_frames

    # endregion Properties
