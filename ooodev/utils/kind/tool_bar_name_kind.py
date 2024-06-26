from __future__ import annotations
from enum import Enum
from ooodev.utils.kind import kind_helper


class ToolBarNameKind(str, Enum):
    THREE_D_OBJECTS_BAR = "3dobjectsbar"
    ADDON_LIBRE_LOGO_OFFICE_TOOL = "addon_LibreLogo.OfficeToolBar"
    ALIGNMENT_BAR = "alignmentbar"
    ARROWS_BAR = "arrowsbar"
    ARROW_SHAPES = "arrowshapes"
    BASIC_SHAPES = "basicshapes"
    BEZIER_OBJECT_BAR = "bezierobjectbar"
    CALL_OUT_SHAPES = "calloutshapes"
    CHANGES = "changes"
    CHOOSE_MODE_BAR = "choosemodebar"
    COLOR_BAR = "colorbar"
    COMMENTS_BAR = "commentsbar"
    COMMON_TASK_BAR = "commontaskbar"
    CONNECTORS_BAR = "connectorsbar"
    CUSTOM_TOOLBAR_1 = "custom_toolbar_1"
    DATASTREAMS = "datastreams"
    DESIGN_OBJECT_BAR = "designobjectbar"
    DIALOG_BAR = "dialogbar"
    DRAW_BAR = "drawbar"
    DRAWING_OBJECT_BAR = "drawingobjectbar"
    DRAW_OBJECT_BAR = "drawobjectbar"
    DRAW_TEXT_OBJECT_BAR = "drawtextobjectbar"
    ELLIPSES_BAR = "ellipsesbar"
    EXTRUSION_OBJECT_BAR = "extrusionobjectbar"
    FIND_BAR = "findbar"
    FLOW_CHART_SHAPES = "flowchartshapes"
    FONT_WORK_OBJECT_BAR = "fontworkobjectbar"
    FONT_WORK_SHAPE_TYPE = "fontworkshapetype"
    FORMAT_OBJECT_BAR = "formatobjectbar"
    FORMATTING = "Formatting"
    FORM_CONTROLS = "formcontrols"
    FORM_CONTROLS_BAR = "formcontrolsbar"
    FORM_DESIGN = "formdesign"
    FORM_OBJECT_BAR = "formobjectbar"
    FORMS_FILTER_BAR = "formsfilterbar"
    FORMS_NAVIGATION_BAR = "formsnavigationbar"
    FORM_TEXT_OBJECT_BAR = "formtextobjectbar"
    FRAME_OBJECT_BAR = "frameobjectbar"
    FULL_SCREEN_BAR = "fullscreenbar"
    GLUE_POINTS_OBJECT_BAR = "gluepointsobjectbar"
    GRAF_FILTER_BAR = "graffilterbar"
    GRAPH_ICO_OBJECT_BAR = "graphicobjectbar"
    INSERT_BAR = "insertbar"
    INSERT_CELLS_BAR = "insertcellsbar"
    INSERT_CONTROLS_BAR = "insertcontrolsbar"
    INSERT_OBJECT_BAR = "insertobjectbar"
    LINES_BAR = "linesbar"
    MACRO_BAR = "macrobar"
    MASTER_VIEW_TOOLBAR = "masterviewtoolbar"
    MEDIA_OBJECT_BAR = "mediaobjectbar"
    MORE_FORM_CONTROLS = "moreformcontrols"
    NAVIGATION_OBJECT_BAR = "navigationobjectbar"
    NUM_OBJECT_BAR = "numobjectbar"
    OLE_OBJECT_BAR = "oleobjectbar"
    OPTIMIZE_TABLE_BAR = "optimizetablebar"
    OPTIONS_BAR = "optionsbar"
    OUTLINE_TOOLBAR = "outlinetoolbar"
    POSITION_BAR = "positionbar"
    PREVIEW_BAR = "previewbar"
    PREVIEW_OBJECT_BAR = "previewobjectbar"
    QUERY_OBJECT_BAR = "queryobjectbar"
    RECTANGLES_BAR = "rectanglesbar"
    REPORT_CONTROLS = "reportcontrols"
    REPORT_OBJECT_BAR = "reportobjectbar"
    RESIZE_BAR = "resizebar"
    SECTION_ALIGNMENT_BAR = "sectionalignmentbar"
    SECTION_SHRINK_BAR = "sectionshrinkbar"
    SLIDE_VIEW_OBJECT_BAR = "slideviewobjectbar"
    SLIDE_VIEW_TOOL_BAR = "slideviewtoolbar"
    SQL_OBJECT_BAR = "sqlobjectbar"
    STANDARD_BAR = "standardbar"
    STAR_SHAPES = "starshapes"
    SYMBOL_SHAPES = "symbolshapes"
    TABLE_OBJECT_BAR = "tableobjectbar"
    TEXT_BAR = "textbar"
    TEXT_OBJECT_BAR = "textobjectbar"
    TOOLBAR = "toolbar"
    TRANSLATION_BAR = "translationbar"
    VIEWER_BAR = "viewerbar"
    ZOOM_BAR = "zoombar"

    def __str__(self) -> str:
        return self.value

    @staticmethod
    def from_str(s: str) -> "ToolBarNameKind":
        """
        Gets an ``ToolBarNameKind`` instance from string.

        Args:
            s (str): String that represents the name of an enum Name.

        Raises:
            ValueError: If input string is empty.
            AttributeError: If unable to get ``ToolBarNameKind`` instance.

        Returns:
            ToolBarNameKind: Enum instance.
        """
        return kind_helper.enum_from_string(s, ToolBarNameKind)
