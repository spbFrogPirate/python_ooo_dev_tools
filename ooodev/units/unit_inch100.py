from __future__ import annotations
from typing import TypeVar, Type
from dataclasses import dataclass
from ooodev.utils.data_type.base_float_value import BaseFloatValue
from .unit_convert import UnitConvert, UnitLength

_TUnitInch100 = TypeVar(name="_TUnitInch100", bound="UnitInch100")


@dataclass(unsafe_hash=True)
class UnitInch100(BaseFloatValue):
    """
    Unit in ``1/100th in`` units.

    Supports ``UnitObj`` protcol.

    See Also:
        :ref:`proto_unit_obj`
    """

    def __post_init__(self):
        if not isinstance(self.value, float):
            object.__setattr__(self, "value", float(self.value))

    def get_value_mm(self) -> float:
        """
        Gets instance value converted to Size in ``mm`` units.

        Returns:
            int: Value in ``mm`` units.
        """
        return UnitConvert.convert(num=self.value, frm=UnitLength.IN100, to=UnitLength.MM)

    def get_value_mm100(self) -> int:
        """
        Gets instance value converted to Size in ``1/100th mm`` units.

        Returns:
            int: Value in ``1/100th mm`` units.
        """
        return round(UnitConvert.convert(num=self.value, frm=UnitLength.IN100, to=UnitLength.MM100))

    def get_value_px(self) -> float:
        """
        Gets instance value in ``px`` (pixel) units.

        Returns:
            int: Value in ``px`` units.
        """
        return UnitConvert.convert(num=self.value, frm=UnitLength.IN100, to=UnitLength.PX)

    def get_value_pt(self) -> float:
        """
        Gets instance value converted to Size in ``pt`` (points) units.

        Returns:
            int: Value in ``pt`` units.
        """
        return UnitConvert.convert(num=self.value, frm=UnitLength.IN100, to=UnitLength.PT)

    @classmethod
    def from_mm100(cls: Type[_TUnitInch100], value: int) -> _TUnitInch100:
        """
        Get instance from ``1/100th mm`` value.

        Args:
            value (int): ``1/100th mm`` value.

        Returns:
            UnitInch100:
        """
        inst = super(UnitInch100, cls).__new__(cls)
        inst.__init__(UnitConvert.convert(num=value, frm=UnitLength.MM100, to=UnitLength.IN100))
        return inst

    @classmethod
    def from_pt(cls: Type[_TUnitInch100], value: float) -> _TUnitInch100:
        """
        Get instance from ``pt`` (points) value.

        Args:
            value (float): ``pt`` value.

        Returns:
            UnitInch100:
        """
        inst = super(UnitInch100, cls).__new__(cls)
        inst.__init__(float(UnitConvert.convert(num=value, frm=UnitLength.PT, to=UnitLength.IN100)))
        return inst

    @classmethod
    def from_px(cls: Type[_TUnitInch100], value: float) -> _TUnitInch100:
        """
        Get instance from ``px`` (pixel) value.

        Args:
            value (float): ``px`` value.

        Returns:
            UnitInch100:
        """
        inst = super(UnitInch100, cls).__new__(cls)
        inst.__init__(UnitConvert.convert(num=value, frm=UnitLength.PX, to=UnitLength.IN100))
        return inst

    @classmethod
    def from_in(cls: Type[_TUnitInch100], value: float) -> _TUnitInch100:
        """
        Get instance from ``in`` (inch) value.

        Args:
            value (float): ``in`` value.

        Returns:
            UnitInch100:
        """
        inst = super(UnitInch100, cls).__new__(cls)
        inst.__init__(UnitConvert.convert(num=value, frm=UnitLength.IN, to=UnitLength.IN100))
        return inst

    @classmethod
    def from_inch10(cls: Type[_TUnitInch100], value: float) -> _TUnitInch100:
        """
        Get instance from ``1/10th in`` (inch) value.

        Args:
            value (int): ``1/10th in`` value.

        Returns:
            UnitInch100:
        """
        inst = super(UnitInch100, cls).__new__(cls)
        inst.__init__(UnitConvert.convert(num=value, frm=UnitLength.IN10, to=UnitLength.IN100))
        return inst

    @classmethod
    def from_inch100(cls: Type[_TUnitInch100], value: float) -> _TUnitInch100:
        """
        Get instance from ``1/10th in`` (inch) value.

        Args:
            value (int): ``1/10th in`` value.

        Returns:
            UnitInch100:
        """
        inst = super(UnitInch100, cls).__new__(cls)
        inst.__init__(value)
        return inst

    @classmethod
    def from_inch1000(cls: Type[_TUnitInch100], value: int) -> _TUnitInch100:
        """
        Get instance from ``1/1,000th in`` (inch) value.

        Args:
            value (int): ``1/1,000th in`` value.

        Returns:
            UnitInch100:
        """
        inst = super(UnitInch100, cls).__new__(cls)
        inst.__init__(UnitConvert.convert(num=value, frm=UnitLength.IN1000, to=UnitLength.IN100))
        return inst
