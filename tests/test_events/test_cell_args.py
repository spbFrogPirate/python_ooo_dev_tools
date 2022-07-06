from __future__ import annotations
from typing import Any

from hypothesis import given, settings
from hypothesis.strategies import text, characters, integers


@given(
    text(
        alphabet=characters(min_codepoint=95, max_codepoint=122, blacklist_characters=("`",)), min_size=3, max_size=25
    ),
    integers(min_value=-100, max_value=100),
)
@settings(max_examples=50)
def test_trigger_event(name: str, value: int):
    from ooodev.events.args.calc.cell_args import CellArgs
    from ooodev.events.lo_events import Events

    cell_args = CellArgs(test_trigger_event)
    cell_args.sheet = None

    def triggered(source: Any, args: CellArgs):
        assert source is test_trigger_event
        cell_args.event_data = value
        cell_args.cells = value
        assert args.event_data == value
        assert args.source is test_trigger_event

    events = Events()
    events.on(name, triggered)
    events.trigger(name, cell_args)
    assert cell_args.event_name == name
    assert cell_args.event_data == value
    assert cell_args.sheet is None
    assert cell_args.cells == value

@given(
    text(
        alphabet=characters(min_codepoint=95, max_codepoint=122, blacklist_characters=("`",)), min_size=3, max_size=25
    ),
    integers(min_value=-100, max_value=100),
)
@settings(max_examples=10)
def test_from_args(name:str, value: int):
    from ooodev.events.args.calc.cell_args import CellArgs
    eargs = CellArgs(test_from_args)
    eargs.event_data = value
    eargs._event_name = name
    eargs.cells = value
    eargs.sheet = None
    
    assert eargs.event_name == name
    assert eargs.event_data == value
    assert eargs.cells == value
    assert eargs.source is test_from_args

    e = CellArgs.from_args(eargs)
    assert e.event_data == eargs.event_data
    assert e.source is eargs.source
    assert e.event_name == eargs.event_name
    assert e.cells == eargs.cells
    assert e.sheet is eargs.sheet
    