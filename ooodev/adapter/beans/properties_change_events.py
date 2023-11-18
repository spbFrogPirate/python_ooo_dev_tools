from __future__ import annotations

from ooodev.adapter.adapter_base import GenericArgs
from ooodev.events.args.listener_event_args import ListenerEventArgs
from ooodev.utils import gen_util as gUtil
from ooodev.utils.type_var import EventArgsCallbackT, ListenerEventCallbackT
from .properties_change_listener import PropertiesChangeListener


class PropertiesChangeEvents:
    """
    Class for managing Properties Change Events.
    """

    def __init__(
        self,
        trigger_args: GenericArgs | None = None,
        cb: ListenerEventCallbackT | None = None,
        listener: PropertiesChangeListener | None = None,
    ) -> None:
        """
        Constructor

        Args:
            trigger_args (GenericArgs, optional): Args that are passed to events when they are triggered.
                This only applies if the listener is not passed.
            cb (ListenerEventCallbackT | None, optional): Callback that is invoked when an event is added or removed.
            listener (PropertiesChangeListener | None, optional): Listener that is used to manage events.
        """
        self.__callback = cb
        if listener:
            self.__listener = listener
        else:
            self.__listener = PropertiesChangeListener(trigger_args=trigger_args)
        self.__name = gUtil.Util.generate_random_string(10)

    # region Manage Events
    def add_event_properties_change(self, cb: EventArgsCallbackT) -> None:
        """
        Adds a listener for an event.

        Event Is invoked when bound properties are changed.

        The callback ``EventArgs.event_data`` will contain a tuple of ``PropertyChangeEvent`` objects.
        """
        if self.__callback:
            args = ListenerEventArgs(source=self.__name, trigger_name="propertiesChange")
            self.__callback(self, args)
            if args.remove_callback:
                self.__callback = None
        self.__listener.on("propertiesChange", cb)

    def remove_event_properties_change(self, cb: EventArgsCallbackT) -> None:
        """
        Removes a listener for an event
        """

        if self.__callback:
            args = ListenerEventArgs(source=self.__name, trigger_name="propertiesChange", is_add=False)
            self.__callback(self, args)
            if args.remove_callback:
                self.__callback = None
        self.__listener.off("propertiesChange", cb)

    # endregion Manage Events

    @property
    def events_listener_properties_change(self) -> PropertiesChangeEvents:
        """
        Returns listener
        """
        return self.__listener