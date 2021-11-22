import sys

import requests
from os import path as OsPath
from constants import *
import json
DEBUG = False

def get_options():
    if DEBUG:
        return {"access_token" : DEFAULT_TOKEN, "user_ids" : DEFAULT_USER_ID,
                "report_format" : DEFAULT_REPORT_FORMAT, "report_path" : DEFAULT_REPORT_PATH()}
    token = input("Enter token:\t")
    test_response = requests.get(f"https://api.vk.com/method/users.get?user_id=1&access_token={token}&v={V}")
    error = response_testing(test_response)
    while error:
        print(error)
        token = input("Enter valid token:\t")
        if token == "exit":
            return []
        error = response_testing(
            requests.get(f"https://api.vk.com/method/users.get?user_id=1&access_token={token}&v={V}"))
    user_id = input("Enter user id:\t")
    test_response = requests.get(f"https://api.vk.com/method/users.get?user_id={user_id}&access_token={token}&v={V}")
    error = response_testing(test_response)
    while error:
        print(error)
        user_id = input("Enter valid user id:\t")
        if user_id == "exit":
            return []
        error = response_testing(
            requests.get(f"https://api.vk.com/method/users.get?user_id={user_id}&access_token={token}&v={V}"))
    report_format = input("Enter format of report(csv,tsv,json) or leave blank for default(csv): ")
    while report_format not in ("csv", "json", "tsv", ""):
        report_format = input("Please choose one of the three formats (csv,json,tsv):")
        if report_format == "exit":
            return []
    if report_format == "":
        report_format = "csv"
    report_path = input("Where to save report(leave blank for current directory): ")
    while not path.exists(report_path):
        if report_path == "":
            report_path = path.dirname(path.abspath(__file__))
            break
        report_path = input("Please enter correct path or leave blank for current directory: ")

    return {"access_token" : token, "user_ids" : user_id,
                "report_format" : report_format, "report_path" : report_path}


def write_to_file(fields: tuple, user: dict = None, report_format: str = "csv", path: str = "", mode="w",
                  separator=",") -> str:
    if not path:
        path = OsPath.dirname(getcwd())
    if not OsPath.exists(path):
        return "Wrong file path"
    file_name = "report." + report_format
    try:
        file = open(path + "\\" + file_name, mode, encoding=sys.getdefaultencoding())
    except PermissionError:
        print("You have no permission to write to this file")
        return "No permission"
    str_to_write_list = []
    if mode == 'w' and report_format != "json":
        for field in fields:
            if type(field) is dict:
                str_to_append = ""
                field = list(field.keys())[0]
            str_to_write_list.append(field)
    elif mode=='w' and report_format == "json":
        str_to_write_list.append('"friends": {')
    else:
        for field in fields:
            if type(field) is dict:
                for in_key in field.keys():
                    try:
                        test = user[in_key]
                        str_to_write_list.append(user[in_key][field[in_key]])
                    except KeyError:
                        str_to_write_list.append("No data")
            else:
                try:
                    test = user[field]
                    if field == "bdate":
                        str_to_append = date_format(user[field])
                    elif field == "sex":
                        str_to_append = SEX_DICT[user[field]]
                    else:
                        str_to_append = str(user[field])
                    str_to_write_list.append(str_to_append)
                except KeyError:
                    str_to_write_list.append("No data")
    try:
        file.write(separator.join(str_to_write_list) + "\n")
    except UnicodeEncodeError:
        print(str_to_write_list)
        sys.exit(10)
    file.close()
    return ""


def date_format(date_to_format: str, date_format: str = "ISO", sep: str = ".", sep_new="-") -> str:
    date_list = date_to_format.split(sep)
    if len(date_list) == 2:
        date_list.append("None")
    return sep_new.join(date_list[::-1])


def response_testing(response: requests.Response) -> str:
    response_json = response.json()
    if "error" in response_json.keys():
        error_code = response_json["error"]["error_code"]
        error_message = response_json["error"]["error_msg"]
        try:
            result = str(ERROR_CODES[error_code])
        except KeyError:
            result = f"Unknown error with code {error_code}, error_msg = {error_message}"
    else:
        result = ""
    return result


