from __future__ import annotations
from typing import TYPE_CHECKING
import contextlib
from dataclasses import dataclass
from ooodev.utils.data_type.base_int_value import BaseIntValue

if TYPE_CHECKING:
    from ooodev.units.angle_t import AngleT


def _to_positive_angle(angle: int) -> int:
    if not isinstance(angle, int):
        raise TypeError(f"Expected type int for angle. Got {type(angle).__name__}")
    # coverts all ints, negative or positive into a positive angle.
    # eg: -10 becomes 350, 380 becomes 20
    return (3600000 + angle) % 360


@dataclass(unsafe_hash=True)
class Angle(BaseIntValue):
    """
    Represents an angle value from ``0`` to ``359``.

    All input integers are converted into a positive angle.

    Example:
        .. code-block::

            >>> print(Angle(360))
            Angle(Value=0)
            >>> print(Angle(413))
            Angle(Value=53)
            >>> print(Angle(-235))
            Angle(Value=125)
            >>> print(Angle(1794))
            Angle(Value=354)

    .. versionchanged:: 0.8.1

        Now will accept any integer value, negative or positive.
    """

    def __post_init__(self) -> None:
        self.value = _to_positive_angle(self.value)

    def _from_int(self, value: int) -> Angle:
        return Angle(_to_positive_angle(value))

    def __eq__(self, other: object) -> bool:
        # for some reason BaseIntValue __eq__ is not picked up.
        # I suspect this is due to this class being a dataclass.
        if isinstance(other, Angle):
            return self.value == other.value
        with contextlib.suppress(AttributeError):
            return self.get_angle100() == other.get_angle100()  # type: ignore
        if isinstance(other, int):
            return self.value == other
        return False

    def get_angle(self) -> int:
        """
        Gets Angle Value as ``degrees``

        .. versionadded:: 0.17.4
        """
        return self.value

    def get_angle10(self) -> int:
        """Gets Angle Value as ``1/10 degree``"""
        return self.value * 10

    def get_angle100(self) -> int:
        """Gets Angle Value as ``1/100 degree``"""
        return self.value * 100

    @staticmethod
    def from_angle(value: int) -> Angle:
        """
        Get an angle from ``degree`` units.

        Args:
            value (int): Angle in ``degree`` units.

        Returns:
            Angle:
        """
        return Angle(0) if value == 0 else Angle(value)

    @staticmethod
    def from_angle10(value: int) -> Angle:
        """
        Get an angle from ``1/10 degree`` units.

        Args:
            value (int): Angle in ``1/10 degree`` units.

        Returns:
            Angle:
        """
        return Angle(0) if value == 0 else Angle(round(value / 10))

    @staticmethod
    def from_angle100(value: int) -> Angle:
        """
        Get an angle from ``1/100 degree`` units.

        Args:
            value (int): Angle in ``1/10 degree`` units.

        Returns:
            Angle:
        """
        return Angle(0) if value == 0 else Angle(round(value / 100))

    @classmethod
    def from_unit_val(cls, value: AngleT | int) -> Angle:
        """
        Get instance from ``Angle`` or int value.

        Args:
            value (Angle, int): ``Angle`` or int value. If int then it is assumed to be in degrees.

        Returns:
            Angle:

        .. versionadded:: 0.32.0
        """
        try:
            unit = value.get_angle()  # type: ignore
            return cls.from_angle(unit)
        except AttributeError:
            return cls.from_angle(int(value))  # type: ignore
