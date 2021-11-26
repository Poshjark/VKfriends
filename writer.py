import sys
from formatters import *

def write_to_file(report_path: str, fields: tuple, user: dict = None, report_format: str = "csv", mode="w",
                  report_name="report", head_or_tail="") -> str:
    """
    Gets path where to save report and depending on format writes firstly head then users data and then tail.

    :param report_path: Where to save file. It can be full path to file or directory
    :param fields: fields from response to write in report
    :param user: dict object with fields like {"name": "John", "last_name": "Smith"}
    :param report_format: format of report (now implemented csv,tsv and json)
    :param mode: mode to open file with  'w' mode used just to write beginning
    :param report_name: name of future report
    :param head_or_tail: used to write head or tail of the report.
    :return: if successful returns empty string. Else returns what's wrong.
    """
    if path.isfile(report_path):
        full_path = report_path
    else:
        full_path = path.join(report_path, report_name + "." + report_format)
    try:
        file = open(full_path, mode, encoding=sys.getdefaultencoding())
    except PermissionError:
        print("You have no permission to write to this file")
        return "No permission"
    if user is None:
        if head_or_tail == "head":
            if FORMATS[report_format]["file_start"] == "fields":
                str_list = list()
                for field in fields:
                    if type(field) is dict:
                        str_list.append(list(field.keys())[0])
                    else:
                        str_list.append(field)
                str_to_write = FORMATS[report_format]["options_separator"].join(str_list)
                str_to_write += FORMATS[report_format]["object_separator"]
            else:
                str_to_write = FORMATS[report_format]["file_start"]
        elif head_or_tail == "tail":
            str_to_write = FORMATS[report_format]["file_end"]
        else:
            str_to_write = ""
    else:
        str_to_write = FORMATS[report_format]["formatter"](user, report_format, fields)
    file.write(str_to_write)
    file.close()
    return ""
