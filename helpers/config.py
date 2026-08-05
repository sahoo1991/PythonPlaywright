import yaml

from helpers.constant import CONFIG_PATH


class ConfigParser:
    def __new__(cls, filename: str, env: str) -> dict:
        with open(CONFIG_PATH.joinpath(filename), encoding="utf-8") as file:
            conf = yaml.load(file, Loader=yaml.FullLoader)
        return conf.get(env)