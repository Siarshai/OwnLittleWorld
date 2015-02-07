import common_utils

def configure_from_file(file_name):
    # Необходимые преобразования данных. Можно вынести в отдельный словарь.
    conversions = {
        "int": lambda x: int(x),
        "float": lambda x: float(x),
        "str": lambda x: x
    }
    # Считываем файл, превращая его в пары {переменная: значение}
    config_dict = {}
    with open(file_name, 'r') as config_file:
        for line in config_file:
            # Никакой проверки - мы любим жить опасно
            variable, value, type = line.split(" ", maxsplit=2)
            if conversions[type] is not None:
                config_dict[variable] = conversions[type](value)
            else:
                print("ERROR: configure from file error at type conversion: ", line)
    for variable in config_dict.keys():
        if common_utils.__getattribute__(variable) is not None:
            common_utils.__setattr__(variable, config_dict[variable])
        else:
            print("WARNING: No such variable: ", variable)