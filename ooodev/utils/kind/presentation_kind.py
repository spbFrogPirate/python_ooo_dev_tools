from .kind_base import KindBase


class PresentationKind(KindBase):
    """
    Values used with ``com.sun.star.presentation.*``

    See Also:
        `Presentation API <https://api.libreoffice.org/docs/idl/ref/namespacecom_1_1sun_1_1star_1_1presentation.html>`_
    """

    CHART_SHAPE = "ChartShape"
    CUSTOM_PRESENTATION = "CustomPresentation"
    CUSTOM_PRESENTATION_ACCESS = "CustomPresentationAccess"
    DATE_TIME_SHAPE = "DateTimeShape"
    DOCUMENT_SETTINGS = "DocumentSettings"
    DRAW_PAGE = "DrawPage"
    FOOTER_SHAPE = "FooterShape"
    GRAPHIC_OBJECT_SHAPE = "GraphicObjectShape"
    HANDOUT_SHAPE = "HandoutShape"
    HANDOUT_VIEW = "HandoutView"
    HEADER_SHAPE = "HeaderShape"
    NOTES_SHAPE = "NotesShape"
    NOTES_VIEW = "NotesView"
    OLE2_SHAPE = "OLE2Shape"
    OUTLINE_VIEW = "OutlineView"
    OUTLINER_SHAPE = "OutlinerShape"
    PAGE_SHAPE = "PageShape"
    PARAGRAPH_TARGET = "ParagraphTarget"
    PRESENTATION = "Presentation"
    PRESENTATION_DOCUMENT = "PresentationDocument"
    PRESENTATION_VIEW = "PresentationView"
    PRESENTATION2 = "Presentation2"
    PREVIEW_VIEW = "PreviewView"
    SHAPE = "Shape"
    SLIDE_NUMBER_SHAPE = "SlideNumberShape"
    SLIDE_SHOW = "SlideShow"
    SLIDES_VIEW = "SlidesView"
    SUBTITLE_SHAPE = "SubtitleShape"
    TITLE_TEXT_SHAPE = "TitleTextShape"
    TRANSITION_FACTORY = "TransitionFactory"

    def to_namespace(self) -> str:
        """Gets full name-space value of instance"""
        return f"com.sun.star.presentation.{self.value}"
