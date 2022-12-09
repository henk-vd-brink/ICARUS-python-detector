import pathlib


class FileSystem:
    def __init__(self, config) -> None:
        self._config = config
        self._parse_config(config)

    def _parse_config(self, config):
        self._file_system_path = config["file_system_path"]

    def get_file_bytes_from_file_name(self, file_name: str):
        with open(self._file_system_path + "/" + file_name, "rb") as file:
            file_bytes = file.read()
        return file_bytes

    def delete_file_bytes_from_file_name(self, file_name: str):
        pathlib.Path(self._file_system_path + "/" + file_name).unlink()
