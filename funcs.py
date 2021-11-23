import sys

import requests
from os import path, getcwd
from formatters import *
from constants import *
DEBUG = False


def get_friends(fields: dict = DEFAULT_FIELDS):
    method = "friends.get"
    options = get_options()
    report_path = options.pop("report_path")
    report_format = options.pop("report_format")
    file_name = options.pop("file_name")
    request_params = options.copy()
    request_params.update({"v": API_VK_VERSION})
    request_params.update({"fields": DEFAULT_FIELDS})
    response = requests.get(f"https://api.vk.com/method/{method}", params=request_params)
    error = response_testing(response)
    if error:
        print(error)
        sys.exit(100)
    js_response = response.json()
    writing = write_to_file(report_path,
                            REQUIRED_ATTRIBUTES,
                            report_format=report_format,
                            mode="w",
                            head_or_tail="head")
    while not writing == "":
        test = input("Please close file and type 'continue' to try to continue writing or type 'exit' to abort:1\t")
        if test == "continue":
            continue
        else:
            while test != "continue":
                print("Type 'continue' to try to continue writing or type 'exit' to abort2")
                test = input()
                if test == "exit":
                    sys.exit(1)
        writing = write_to_file(report_path,
                                REQUIRED_ATTRIBUTES,
                                report_format=report_format,
                                mode="w",
                                head_or_tail="head")
    for user in js_response['response']['items']:
        while not write_to_file(report_path, REQUIRED_ATTRIBUTES, user, report_format=report_format, mode="a") == "":
            print("Please close file and type 'continue' to continue writing")
            test = input()
            if test == "continue":
                continue
            else:
                while test != "continue":
                    print("Type 'continue' to try to continue writing or type 'exit' to abort  123")
                    test = input()
                    if test == "exit":
                        sys.exit(1)
    write_to_file(report_path,
                  REQUIRED_ATTRIBUTES,
                  user=None,
                  report_format=report_format,
                  mode="a",
                  head_or_tail="tail")
    if path.isfile(report_path):
        print("Report succesfully saved to " + report_path)
    else:
        print("Report succesfully saved to " + path.join(report_path, file_name))


def get_token() -> str:
    token = input("Enter token:\t")
    test_response = requests.get(
        f"https://api.vk.com/method/users.get?user_id=1&access_token={token}&v={API_VK_VERSION}")
    error = response_testing(test_response)
    while error:
        print(error)
        token = input("Enter valid token:\t")
        if token == "exit":
            sys.exit(1)
        error = response_testing(
            requests.get(f"https://api.vk.com/method/users.get?user_id=1&access_token={token}&v={API_VK_VERSION}"))
    return token


def get_user_id(token: str) -> str:
    user_id = input("Enter user_id:\t")
    while not user_id:
        user_id = input("Please enter user_id:\t")
    test_response = requests.get(f"https://api.vk.com/method/users.get?",
                                 params={
                                     "user_id": user_id,
                                     "access_token": token,
                                     "v": API_VK_VERSION

                                 }, )
    error = response_testing(test_response)
    while True:
        while error:
            print(error)
            user_id = input("Enter valid user id:\t")
            if user_id == "exit":
                return sys.exit(1)
            test_response = requests.get(
                f"https://api.vk.com/method/users.get?user_id={user_id}&access_token={token}&v={API_VK_VERSION}")
            error = response_testing(test_response)
        if 'deactivated' in test_response.json()['response'][0].keys():
            user_id = input("Profile deleted or banned, please choose another id:\t")
            test_response = requests.get(
                f"https://api.vk.com/method/users.get?user_id={user_id}&access_token={token}&v={API_VK_VERSION}")
            error = response_testing(test_response)
            continue
        elif test_response.json()['response'][0]['is_closed']:
            user_id = input("Profile is private, please choose another id:\t")
            test_response = requests.get(
                f"https://api.vk.com/method/users.get?user_id={user_id}&access_token={token}&v={API_VK_VERSION}")
            error = response_testing(test_response)
            continue
        else:
            break
    return user_id


def get_report_format() -> str:
    report_format = input("Enter format of report(csv,tsv,json) or leave blank for default(csv): ")
    while report_format not in ("csv", "json", "tsv", ""):
        report_format = input("Please choose one of the three formats (csv,json,tsv):")
        if report_format == "exit":
            sys.exit(1)
    if report_format == "":
        report_format = "csv"
    return report_format


def get_report_path() -> str:
    report_path = input("Where to save report(leave blank for current directory): ")
    if path.isfile(report_path):
        return report_path
    while not path.exists(report_path):
        if report_path == "":
            report_path = getcwd()
            break
        try:
            open(report_path, 'r')
        except FileNotFoundError:
            print("reportpath = ", report_path)
            try:
                open(report_path, 'w')
                return report_path
            except PermissionError:
                print("No rights to create file here")
        report_path = input("Please enter correct path or leave blank for current directory: ")
        if report_path == 'exit':
            sys.exit(1)
    return report_path


def get_options():
    if DEBUG:
        return {"access_token": DEFAULT_TOKEN, "user_id": DEFAULT_USER_ID,
                "report_format": DEFAULT_REPORT_FORMAT, "report_path": DEFAULT_REPORT_PATH()}
    token = get_token()
    user_id = get_user_id(token)
    report_format = get_report_format()
    report_path = get_report_path()
    if path.isfile(report_path):
        file_name = path.basename(report_path)
    else:
        file_name = "report." + report_format

    return {"access_token": token,
            "report_format": report_format,
            "report_path": report_path,
            "user_id": user_id,
            "file_name": file_name
            }


def write_to_file(report_path: str, fields: tuple, user: dict = None, report_format: str = "csv", mode="w",
                  report_name="report", head_or_tail = "") -> str:
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
