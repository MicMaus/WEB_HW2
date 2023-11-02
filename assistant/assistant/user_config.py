from collections import UserDict
from pathlib import Path


class Config(UserDict):
    def __init__(self, config_file: str) -> None:
        super().__init__()
        self.__config_file = None
        self.config_file = config_file

    @property
    def config_file(self):
        return self.__config_file

    @config_file.setter
    def config_file(self, config_file: str) -> None:
        config_path = Path(config_file)
        if config_path.exists():
            self.__config_file = config_file
            self.read_config()

    def read_config(self) -> None:
        with open(self.config_file, "r") as f:
            for line in f:
                try:
                    key, value = line.split("=")
                except:
                    continue
                self.data[key] = value.replace("\n", "")

    def save_config(self) -> None:
        with open(self.config_file, "w") as f:
            for key, value in self.data.items():
                f.write(f"{key}={value}\n")
