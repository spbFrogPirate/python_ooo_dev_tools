# coding: utf-8
from __future__ import annotations
from typing import Any
from .dispatch_args import DispatchArgs
from .cancel_event_args import CancelEventArgs


class DispatchCancelArgs(DispatchArgs, CancelEventArgs):
    """
    Dispatch Cancel Args
    """

    def __init__(self, source: Any, cmd: str, cancel=False) -> None:
        """
        Constructor

        Args:
            source (Any): Event Source
            cmd (str): Event Dispatch Command
            cancel (bool, optional): Cancel value. Defaults to False.
        """
        super().__init__(source=source, cmd=cmd)
        self.cancel = cancel

    @staticmethod
    def from_args(args: DispatchCancelArgs) -> DispatchCancelArgs:
        """
        Gets a new instance from existing instance

        Args:
            args (DispatchCancelArgs): Existing Instance

        Returns:
            DispatchCancelArgs: args
        """
        eargs = DispatchCancelArgs(source=args.source, cmd=args.cmd)
        eargs.event_data = args.event_data
        eargs.cancel = args.cancel
        return args
