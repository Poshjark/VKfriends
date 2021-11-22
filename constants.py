from os import path,getcwd

ERROR_CODES = {5: "Invalid token", 113: "Invalid user id", 100: "User id not integer, please enter integer"}


REQUIRED_ATTRIBUTES = ("first_name", "last_name", {"country" : "title"}, {"city" : "title"}, "bdate", "sex")

V = "5.131"

SEX_DICT = {0: "No data", 1: "Female", 2: "Male", "0": "No data", "1": "Female", "2": "Male"}

DEFAULT_TOKEN = ""
DEFAULT_USER_ID = "1"
DEFAULT_REPORT_FORMAT = "csv"
DEFAULT_FIELDS = "bdate"
API_MAIN_REF = "https://api.vk.com/method/"
API_VK_VERSION = "5.131"
DEFAULT_LANGUAGE = 0
FORMATS = {"json" : {"options_separator" : ",\n", "object_separator" : "\n},", "start" : "{\n\t"},
           "csv" : {"options_separator" : ",", "object_separator" : "\n", "start" : ""},
           "tsv" : {"options_separator" : "\t", "object_separator" : "\n", "start" : ""},
           }

def DEFAULT_REPORT_PATH() -> str:
    return path.dirname(getcwd())