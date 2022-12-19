import pathlib
import logging
import numpy as np


class FileSystem:
    def __init__(self, config) -> None:
        self._config = config
        self._parse_config(config)

        self._logger = logging.getLogger(__name__)

    def _parse_config(self, config):
        self._file_system_path = config["file_system_path"]

    def get_file_bytes_from_file_name(self, file_name: str):
        with open(self._file_system_path + "/" + file_name, "rb") as file:
            file_bytes = file.read()
        return file_bytes

    def get_numpy_array_from_file_name(self, file_name: str):
        try:
            return self._get_numpy_array_from_file_name(file_name)
        except Exception as e:
            self._logger.exception(e)
            return None

    def _get_numpy_array_from_file_name(self, file_name: str):
        with open(self._file_system_path + "/" + file_name, "rb") as file:
            numpy_array = np.load(file)
        return numpy_array

    def delete_file_bytes_from_file_name(self, file_name: str):
        pathlib.Path(self._file_system_path + "/" + file_name).unlink()
