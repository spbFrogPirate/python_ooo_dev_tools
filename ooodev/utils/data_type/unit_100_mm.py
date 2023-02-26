from __future__ import annotations
from typing import TypeVar, Type
from dataclasses import dataclass
from ..validation import check
from ..decorator import enforce
from .base_int_value import BaseIntValue
from ..unit_convert import UnitConvert, Length

_TUnit100MM = TypeVar(name="_TUnit100MM", bound="Unit100MM")

# Note that from __future__ import annotations converts annotations to string.
# this means that @enforce.enforce_types will see string as type. This is fine in
# most cases. Especially for built in types.
@enforce.enforce_types
@dataclass(unsafe_hash=True)
class Unit100MM(BaseIntValue):
    """Represents ``mm`` units."""

    def __post_init__(self) -> None:
        check(
            self.value >= 0,
            f"{self}",
            f"Value of {self.value} is out of range. Value must be a positive number.",
        )

    def _from_int(self, value: int) -> _TUnit100MM:
        inst = super(Unit100MM, self.__class__).__new__(self.__class__)
        return inst.__init__(value)

    def __eq__(self, other: object) -> bool:
        # for some reason BaseIntValue __eq__ is not picked up.
        # I suspect this is due to this class being a dataclass.
        try:
            i = int(other)
            return i == self.value
        except Exception as e:
            return False

    def get_value_mm(self) -> float:
        """
        Gets instance value converted to Size in ``mm`` units.

        Returns:
            int: Value in ``mm`` units.
        """
        return UnitConvert.convert_mm100_mm(self.value)

    def get_value_pt(self) -> float:
        """
        Gets instance value converted to Size in ``pt`` (point) units.

        Returns:
            int: Value in ``pt`` units.
        """
        return round(UnitConvert.convert(num=self.value, frm=Length.MM100, to=Length.PT))

    @classmethod
    def from_mm(cls: Type[_TUnit100MM], value: float) -> _TUnit100MM:
        """
        Get instance from ``mm`` value.

        Args:
            value (int): ``mm`` value.

        Returns:
            Unit100MM:
        """
        inst = super(Unit100MM, cls).__new__(cls)
        return inst.__init__(UnitConvert.convert_mm_mm100(value))

    @classmethod
    def from_pt(cls: Type[_TUnit100MM], value: int) -> _TUnit100MM:
        """
        Get instance from ``pt`` (points) value.

        Args:
            value (int): ``pt`` value.

        Returns:
            Unit100MM:
        """
        inst = super(Unit100MM, cls).__new__(cls)
        return inst.__init__(round(UnitConvert.convert(num=value, frm=Length.PT, to=Length.MM100)))
