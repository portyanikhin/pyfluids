from __future__ import annotations

import json
import tomllib
from configparser import ConfigParser
from dataclasses import dataclass
from os.path import abspath
from pathlib import Path
from typing import NoReturn, cast

from .singleton import Singleton
from .units_system import UnitsSystem

__all__ = ["Config", "ConfigBuilder"]


@dataclass
class Config:
    """pyfluids configuration."""

    units_system: UnitsSystem = UnitsSystem.SIWithCelsiusAndPercents


# noinspection PyBroadException
class ConfigBuilder(metaclass=Singleton):
    """pyfluids configuration builder."""

    def __init__(self):
        """pyfluids configuration builder."""
        self.__config: Config | None = None
        self.__config_names: list[str] = [
            "pyfluids.ini",
            "pyfluids.json",
            "pyproject.toml",
            "tox.ini",
        ]

    @property
    def __current_path(self) -> Path:
        return Path(abspath(Path.cwd()))

    @property
    def __config_file(self) -> Path | None:
        for root in (self.__current_path, *self.__current_path.parents):
            for config_name in self.__config_names:
                path = root / config_name
                if path.is_file():
                    return path
        return None

    @property
    def __config_data(self) -> str:
        return cast(Path, self.__config_file).read_text(encoding="utf-8")

    def build(self) -> Config:
        """
        Build pyfluids configuration.

        If the configuration file is not found or an incorrect
        configuration is found in the files "pyproject.toml" or "tox.ini",
        returns the default configuration.

        :raises ValueError: If configuration file is invalid.
        """
        if self.__config is not None:
            return self.__config
        if self.__config_file is None:
            return self.__create_default_config()
        if self.__config_file.suffix == ".ini":
            return self.__load_config_from_ini_file()
        if self.__config_file.suffix == ".json":
            return self.__load_config_from_json_file()
        return self.__load_config_from_toml_file()

    def _reset(self):
        self.__config = None

    def __create_default_config(self) -> Config:
        self.__config = Config()
        return self.__config

    def __create_config_from_dict(self, config_dict: dict) -> Config:
        config_dict["units_system"] = UnitsSystem[config_dict["units_system"]]
        self.__config = Config(**config_dict)
        return self.__config

    def __load_config_from_ini_file(self) -> Config:
        try:
            config_parser = ConfigParser()
            config_parser.read(cast(Path, self.__config_file))
            return self.__create_config_from_dict(dict(config_parser.items("pyfluids")))
        except Exception:
            if cast(Path, self.__config_file).name.startswith("pyfluids"):
                self.__raise_invalid_config_exception()
            return self.__create_default_config()

    def __load_config_from_json_file(self) -> Config:
        try:
            return self.__create_config_from_dict(
                json.loads(self.__config_data)["pyfluids"]
            )
        except Exception:
            self.__raise_invalid_config_exception()

    def __load_config_from_toml_file(self) -> Config:
        try:
            return self.__create_config_from_dict(
                tomllib.loads(self.__config_data)["tool"]["pyfluids"]
            )
        except Exception:
            return self.__create_default_config()

    def __raise_invalid_config_exception(self) -> NoReturn:
        raise ValueError(
            "Invalid pyfluids configuration! "
            f"Check your configuration file: {self.__config_file}"
        )
