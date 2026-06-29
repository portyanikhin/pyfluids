from __future__ import annotations

from CoolProp.CoolProp import parameters

from ..config import UnitConverter
from .abstract_input import AbstractInput

__all__ = ["Input"]


class Input(AbstractInput[parameters]):
    """CoolProp keyed input for fluids and mixtures."""

    def __init__(self, coolprop_key: parameters, value: float):
        """
        CoolProp keyed input for fluids and mixtures.

        :param coolprop_key: CoolProp internal key.
        :param value: Input value in SI units.
        """
        super().__init__(coolprop_key, value)

    @classmethod
    def density(cls, value: float) -> Input:
        """
        Mass density.

        :param value: The value of the input [kg/m3].
        :return: Mass density for the input.
        """
        return cls(parameters.iDmass, value)

    @classmethod
    def enthalpy(cls, value: float) -> Input:
        """
        Mass specific enthalpy.

        :param value: The value of the input [J/kg].
        :return: Mass specific enthalpy for the input.
        """
        return cls(parameters.iHmass, value)

    @classmethod
    def entropy(cls, value: float) -> Input:
        """
        Mass specific entropy.

        :param value: The value of the input [J/kg/K].
        :return: Mass specific entropy for the input.
        """
        return cls(parameters.iSmass, value)

    @classmethod
    def internal_energy(cls, value: float) -> Input:
        """
        Mass specific internal energy.

        :param value: The value of the input [J/kg].
        :return: Mass specific internal energy for the input.
        """
        return cls(parameters.iUmass, value)

    @classmethod
    def pressure(cls, value: float) -> Input:
        """
        Absolute pressure.

        :param value: The value of the input [Pa].
        :return: Absolute pressure for the input.
        """
        return cls(parameters.iP, value)

    @classmethod
    def quality(cls, value: float) -> Input:
        """
        Mass vapor quality.

        :param value: The value of the input
            [by default, %; you can change this using the configuration file].
        :return: Mass vapor quality for the input.
        """
        return cls(parameters.iQ, UnitConverter().convert_decimal_fraction_to_si(value))

    @classmethod
    def specific_volume(cls, value: float) -> Input:
        """
        Mass specific volume.

        :param value: The value of the input [m3/kg].
        :return: Mass specific volume for the input.
        """
        return cls(parameters.iDmass, 1 / value)

    @classmethod
    def temperature(cls, value: float) -> Input:
        """
        Temperature.

        :param value: The value of the input
            [by default, °C; you can change this using the configuration file].
        :return: Temperature for the input.
        """
        return cls(parameters.iT, UnitConverter().convert_temperature_to_si(value))
