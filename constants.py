from os import path, getcwd

REQUIRED_ATTRIBUTES = ("first_name", "last_name", {"country": "title"}, {"city": "title"}, "bdate", "sex")
SEX_DICT = {0: "No data", 1: "Female", 2: "Male", "0": "No data", "1": "Female", "2": "Male"}
DEFAULT_TOKEN = ""
DEFAULT_USER_ID = "1"
DEFAULT_REPORT_FORMAT = "csv"
DEFAULT_FIELDS = "bdate,sex"
API_MAIN_REF = "https://api.vk.com/method/"
API_VK_VERSION = "5.131"
DEFAULT_LANGUAGE = 0


def DEFAULT_REPORT_PATH() -> str:
    return path.dirname(getcwd())


ERROR_CODES = {
    1: "Unknown error",
    3: "Unknown method",
    4: "Invalid token",
    5: "Invalid access token",
    7: "No permissions for this action",
    8: "Wrong request",
    10: "Server fault, try again later",
    15: "Access denied",
    18: "Page deleted or banned",
    23: "Method was turned off",
    29: "Number of requests limit reached",
    30: "Profile is private",
    33: "Not implemented yet",
    34: "Client version deprecated",
    37: "User was banned",
    38: "Unknown application",
    39: "Unknown user",
    100: "One of the required parameters was not passed or was incorrect",
    113: "Wrong user id",
    1114: "Anonymous token has expired",
    1116: "Anonymous token is invalid",
    3610: "User is deactivated",

}
