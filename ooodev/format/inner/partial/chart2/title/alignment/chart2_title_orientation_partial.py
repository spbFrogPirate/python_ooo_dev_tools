from __future__ import annotations
from typing import Any, Dict, TYPE_CHECKING
import uno

from ooodev.events.gbl_named_event import GblNamedEvent
from ooodev.events.partial.events_partial import EventsPartial
from ooodev.events.args.cancel_event_args import CancelEventArgs
from ooodev.events.args.event_args import EventArgs
from ooodev.exceptions import ex as mEx

if TYPE_CHECKING:
    from ooodev.format.inner.direct.chart2.title.alignment.orientation import Orientation
    from ooodev.units import Angle


class Chart2TitleOrientationPartial:
    """
    Partial class for Chart2 Data Labels Orientation.
    """

    def __init__(self, component: Any) -> None:
        self.__component = component

    def style_orientation(self, angle: int | Angle | None = None, vertical: bool | None = None) -> Orientation | None:
        """
        Style Chart2 Data Series Text Attributes.

        Args:
            angle (int, Angle, optional): Rotation in degrees of the text.
            vertical (bool, optional): Specifies if the text is vertically stacked.

        Raises:
            CancelEventError: If the event ``before_style_chart2_text_orientation`` is cancelled and not handled.

        Returns:
            Orientation | None: Orientation Style instance or ``None`` if cancelled.
        """
        from ooodev.format.inner.direct.chart2.title.alignment.orientation import Orientation

        comp = self.__component
        has_events = False
        cargs = None
        if isinstance(self, EventsPartial):
            has_events = True
            cargs = CancelEventArgs(self.style_orientation.__qualname__)
            event_data: Dict[str, Any] = {
                "angle": angle,
                "vertical": vertical,
                "this_component": comp,
            }
            cargs.event_data = event_data
            self.trigger_event("before_style_chart2_text_orientation", cargs)
            if cargs.cancel is True:
                if cargs.handled is False:
                    cargs.set("initial_event", "before_style_chart2_text_orientation")
                    self.trigger_event(GblNamedEvent.EVENT_CANCELED, cargs)
                    if cargs.handled is False:
                        raise mEx.CancelEventError(cargs, "Style has been cancelled.")
                    else:
                        return None
                else:
                    return None
            angle = cargs.event_data.get("angle", angle)
            vertical = cargs.event_data.get("vertical", vertical)
            comp = cargs.event_data.get("this_component", comp)

        fe = Orientation(
            angle=angle,
            vertical=vertical,
        )

        if has_events:
            fe.add_event_observer(self.event_observer)  # type: ignore

        fe.apply(comp)
        fe.set_update_obj(comp)
        if has_events:
            self.trigger_event("after_style_chart2_text_orientation", EventArgs.from_args(cargs))  # type: ignore
        return fe
