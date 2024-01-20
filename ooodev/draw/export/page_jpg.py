from __future__ import annotations
from typing import Any, cast, Callable, TYPE_CHECKING
import uno

from ooodev.adapter.drawing.graphic_export_filter_implement import GraphicExportFilterImplement
from ooodev.draw import DrawNamedEvent
from ooodev.draw import DrawPage
from ooodev.events.args.cancel_event_args_export import CancelEventArgsExport
from ooodev.events.args.event_args_export import EventArgsExport
from ooodev.events.partial.events_partial import EventsPartial
from ooodev.exceptions import ex as mEx
from ooodev.proto.component_proto import ComponentT
from ooodev.units import UnitInch
from ooodev.utils import file_io as mFile
from ooodev.utils import props as mProps
from ooodev.utils.type_var import PathOrStr  # , EventCallback

if TYPE_CHECKING:
    from ooodev.draw.filter.export_jpg import ExportJpgT
    from com.sun.star.lang import XComponent
else:
    ExportJpgT = Any


class PageJpg(EventsPartial):
    """Class for exporting current Draw page as a jpg image."""

    def __init__(self, owner: DrawPage[ComponentT]):
        EventsPartial.__init__(self)
        self._owner = owner
        self._doc = owner.owner
        self._filter_name = "draw_jpg_Export"

    # def _get_shapes(self) -> ShapeCollection:
    #     comp = ShapeCollection(self)
    #     for shape in self._draw_page:
    #         comp.add(shape.component)
    #     return comp

    def export(self, fnm: PathOrStr, resolution: int = 96) -> None:
        """
        Exports page as jpg image.

        Args:
            fnm (PathOrStr, optional): Image file name.
            resolution (int, optional): Resolution in dpi. Defaults to 96.

        :events:
            .. cssclass:: lo_event

                - :py:attr:`~ooodev.events.draw_named_event.DrawNamedEvent.EXPORTING_PAGE_JPG` :eventref:`src-docs-event-cancel-export`
                - :py:attr:`~ooodev.events.draw_named_event.DrawNamedEvent.EXPORTED_PAGE_JPG` :eventref:`src-docs-event-export`

        Returns:
            None:

        Note:
            On exporting event is :ref:`cancel_event_args_export`.
            On exported event is :ref:`event_args_export`.
            Args ``event_data`` is a :py:class:`~ooodev.write.filter.export_jpg.ExportJpgT` dictionary.

            Unlike exporting png, exporting jpg does not seem to have a limit on the image size.

            Page margins are ignored. Any shape that is outside the page margins will not be included in the image.
        """
        if not fnm:
            raise ValueError("fnm is required")
        # if not isinstance(self._doc, StorablePartial):
        #     raise NotImplementedError(f"StorablePartial is not implemented in: {type(self._doc).__name__}")

        width = self._owner.component.Width
        height = self._owner.component.Height
        width_in = UnitInch.from_mm100(width)
        height_in = UnitInch.from_mm100(height)
        dpi_x = round(resolution * width_in.value)
        dpi_y = round(resolution * height_in.value)

        # if not isinstance(self._doc, StorablePartial):

        # if self._shapes_only:
        #     self._shapes = self._get_shapes()
        #     width = self._shapes.get_width()
        #     height = self._shapes.get_height()
        #     width_in = UnitInch(width.get_value_inch())
        #     height_in = UnitInch(height.get_value_inch())
        #     logical_width = width.get_value_mm100()
        #     logical_height = height.get_value_mm100()
        # else:
        width = self._owner.component.Width
        height = self._owner.component.Height
        width_in = UnitInch.from_mm100(width)
        height_in = UnitInch.from_mm100(height)
        dpi_x = round(resolution * width_in.value)
        dpi_y = round(resolution * height_in.value)

        event_data: ExportJpgT = {
            "color_mode": True,
            "quality": 75,
            "pixel_width": dpi_x,
            "pixel_height": dpi_y,
            "logical_width": width,
            "logical_height": height,
        }

        cargs = CancelEventArgsExport(source=self, event_data=event_data, fnm=fnm, overwrite=True)
        cargs.set("image_type", "jpg")
        cargs.set("filter_name", self._filter_name)

        self.trigger_event(DrawNamedEvent.EXPORTING_PAGE_JPG, cargs)
        if cargs.cancel and cargs.handled is False:
            raise mEx.CancelEventError(cargs)

        make_prop = mProps.Props.make_prop_value
        filter_data = [
            make_prop(name="ColorMode", value=int(not cargs.event_data["color_mode"])),
        ]
        # filter_data_props = PropertyValue("FilterData", 0, uno.Any("[]com.sun.star.beans.PropertyValue", tuple(filter_data)), dv)
        pixel_width = cargs.event_data["pixel_width"]
        pixel_height = cargs.event_data["pixel_height"]
        if pixel_width > 0 and pixel_height > 0:
            filter_data.append(make_prop(name="PixelWidth", value=pixel_width))
            filter_data.append(make_prop(name="PixelHeight", value=pixel_height))

        # quality 1..100 default 75
        quality = cargs.event_data["quality"]
        if quality > 0 and quality < 101:
            filter_data.append(make_prop(name="Quality", value=quality))

        logical_height = cargs.event_data["logical_height"]
        logical_width = cargs.event_data["logical_width"]
        if logical_height > 0 and logical_width > 0:
            filter_data.append(make_prop(name="LogicalHeight", value=logical_height))
            filter_data.append(make_prop(name="LogicalWidth", value=logical_width))

        url = mFile.FileIO.fnm_to_url(fnm=cargs.fnm)

        args = mProps.Props.make_props(
            FilterName=self._filter_name,
            MediaType="image/jpeg",
            URL=url,
            FilterData=uno.Any("[]com.sun.star.beans.PropertyValue", tuple(filter_data)),  # type: ignore
            Overwrite=cargs.overwrite,
        )
        graphic_filter = GraphicExportFilterImplement()
        graphic_filter.set_source_document(cast("XComponent", self._owner.component))
        graphic_filter.filter(*args)

        # if self._shapes_only:
        #     self._export_shapes(args)
        # else:
        #     self._export_doc(args)

        eargs = EventArgsExport.from_args(cargs)
        eargs.set("url", url)
        self.trigger_event(DrawNamedEvent.EXPORTED_PAGE_JPG, eargs)
        self._shapes = None

    # def _export_doc(self, args: tuple) -> None:
    #     graphic_filter = GraphicExportFilterImplement()
    #     graphic_filter.set_source_document(self._draw_page.qi(XComponent, True))
    #     graphic_filter.filter(*args)

    # def _export_shapes(self, args: tuple) -> None:
    #     graphic_filter = GraphicExportFilterImplement()
    #     if self._shapes is None:
    #         shapes = self._get_shapes()
    #     else:
    #         shapes = self._shapes
    #     graphic_filter.set_source_document(shapes.qi(XComponent, True))
    #     graphic_filter.filter(*args)

    # region Events
    def subscribe_event_exporting(self, callback: Callable[[Any, CancelEventArgsExport[ExportJpgT]], None]) -> None:
        """
        Add an event listener to current instance that is triggered on exporting.

        Args:
            callback (Callable[[Any, CancelEventArgsExport[ExportJpgT]], None]): Callback of the event listener.

        Returns:
            None:
        """
        self.subscribe_event(DrawNamedEvent.EXPORTING_PAGE_JPG, callback)

    def subscribe_event_exported(self, callback: Callable[[Any, EventArgsExport[ExportJpgT]], None]) -> None:
        """
        Add an event listener to current instance that is triggered on export complete.

        Args:
            callback (Callable[[Any, EventArgsExport[ExportJpgT]], None]): Callback of the event listener.

        Returns:
            None:
        """
        self.subscribe_event(DrawNamedEvent.EXPORTED_PAGE_JPG, callback)

    def unsubscribe_event_exporting(self, callback: Callable[[Any, CancelEventArgsExport[ExportJpgT]], None]) -> None:
        """
        Remove an event listener from current instance.

        Args:
            callback (Callable[[Any, CancelEventArgsExport[ExportJpgT]], None]): Callback of the event listener.

        Returns:
            None:
        """
        self.unsubscribe_event(DrawNamedEvent.EXPORTING_PAGE_JPG, callback)

    def unsubscribe_event_exported(self, callback: Callable[[Any, EventArgsExport[ExportJpgT]], None]) -> None:
        """
        Remove an event listener from current instance.

        Args:
            callback (Callable[[Any, EventArgsExport[ExportJpgT]], None]): Callback of the event listener.

        Returns:
            None:
        """
        self.unsubscribe_event(DrawNamedEvent.EXPORTED_PAGE_JPG, callback)

    # endregion Events
