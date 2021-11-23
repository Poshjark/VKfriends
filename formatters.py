from constants import *


def format_to_symbol_separated(user: dict, report_format: str, fields: tuple) -> str:
    if user is None:
        str_to_write_list = []
        for field in fields:
            if type(field) is dict:
                for key in field.keys():
                    str_to_write_list.append(key)
            else:
                str_to_write_list.append(field)
    else:
        str_to_write_list = []
        for field in fields:
            if type(field) is dict:
                for in_key in field.keys():
                    try:
                        user[in_key]
                        str_to_write_list.append(user[in_key][field[in_key]])
                    except KeyError:
                        str_to_write_list.append("No data")
            else:
                try:
                    user[field]
                    if field == "bdate":
                        str_to_append = date_format(user[field])
                    elif field == "sex":
                        str_to_append = SEX_DICT[user[field]]
                    else:
                        str_to_append = str(user[field])
                    str_to_write_list.append(str_to_append)
                except KeyError:
                    str_to_write_list.append("No data")
    return FORMATS[report_format]["options_separator"].join(str_to_write_list) + FORMATS[report_format][
        "object_separator"]


def json_formatting(user: dict, report_format: str, fields: tuple) -> str:
    str_to_write_list = []
    for field in fields:
        if type(field) is dict:
            for in_key in field.keys():
                try:
                    user[in_key]
                    str_to_write_list.append(f'"{in_key}" : "{user[in_key][field[in_key]]}"')
                except KeyError:
                    str_to_write_list.append(f'"{in_key}"' + ' : "No data"')
        else:
            try:
                user[field]
                if field == "bdate":
                    str_to_write_list.append(f'"{field}" : "{date_format(user[field])}"')
                elif field == "sex":
                    str_to_write_list.append(f'"{field}" : "{SEX_DICT[user[field]]}"')
                else:
                    str_to_write_list.append(f'"{field}" : "{user[field]}"')
            except KeyError:
                str_to_write_list.append("No data")
    str_to_write_list[0] = FORMATS[report_format]["object_start"] + str_to_write_list[0]
    str_to_write_list[-1] = str_to_write_list[-1] + FORMATS[report_format]["object_end"]
    return FORMATS[report_format]["options_separator"].join(str_to_write_list)


def date_format(date_to_format: str, sep: str = ".", sep_new="-") -> str:
    date_list = date_to_format.split(sep)
    if len(date_list) == 2:
        date_list.append("None")
    return sep_new.join(date_list[::-1])


FORMATS = {"json":
               {"options_separator": ",\n\t\t",
                "object_separator": "\n},",
                "object_start": "\t{\n\t\t",
                "object_end": "\n\t},\n",
                "file_start": '"friends" : {\n',
                "file_end": "}",
                "formatter": json_formatting
                },
           "csv":
               {"options_separator": ",",
                "object_separator": "\n",
                "object_start": "",
                "object_end": "",
                "file_start": "",
                "file_end": "",
                "formatter": format_to_symbol_separated
                },
           "tsv":
               {"options_separator": "\t",
                "object_separator": "\n",
                "object_start": "",
                "object_end": "",
                "file_start": "",
                "file_end": "",
                "formatter": format_to_symbol_separated
                },
           }
