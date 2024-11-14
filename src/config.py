from configparser import ConfigParser
from typing import Dict


def config(filename: str = "database.ini", section: str = "postgresql") -> Dict[str, str]:
    parser = ConfigParser()
    parser.read(filename)

    db = {}

    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception("Значение {0} не найдено в файле {1}.".format(section, filename))
    return db
