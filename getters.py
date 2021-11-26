import sys
import requests

import formatters
from constants import *
import testers

DEBUG = False



def get_token() -> str:
    token = input("Enter token:\t")
    test_response = requests.get(
        f"https://api.vk.com/method/users.get?user_id=1&access_token={token}&v={API_VK_VERSION}")
    error = testers.response_testing(test_response)
    while error:
        print(error)
        token = input("Enter valid token:\t")
        if token == "exit":
            sys.exit(1)
        error = testers.response_testing(
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
    error = testers.response_testing(test_response)
    while True:
        while error:
            print(error)
            user_id = input("Enter valid user id:\t")
            if user_id == "exit":
                return sys.exit(1)
            test_response = requests.get(
                f"https://api.vk.com/method/users.get?user_id={user_id}&access_token={token}&v={API_VK_VERSION}")
            error = testers.response_testing(test_response)
        if 'deactivated' in test_response.json()['response'][0].keys():
            user_id = input("Profile deleted or banned, please choose another id:\t")
            test_response = requests.get(
                f"https://api.vk.com/method/users.get?user_id={user_id}&access_token={token}&v={API_VK_VERSION}")
            error = testers.response_testing(test_response)
            continue
        elif test_response.json()['response'][0]['is_closed']:
            user_id = input("Profile is private, please choose another id:\t")
            test_response = requests.get(
                f"https://api.vk.com/method/users.get?user_id={user_id}&access_token={token}&v={API_VK_VERSION}")
            error = testers.response_testing(test_response)
            continue
        else:
            break
    return user_id


def get_report_format() -> str:
    report_format = input("Enter format of report(csv,tsv,json) or leave blank for default(csv): ")
    if report_format == "":
        report_format = "csv"
    print(formatters.FORMATS.keys())
    while report_format not in formatters.FORMATS.keys() :
        print(f"'{report_format}'")
        report_format = input("Please choose one of the three formats (csv,json,tsv):")
        if report_format == "exit":
            sys.exit(1)
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


def get_options() -> dict:
    """
    Calls other getters and collects results to dict
    :return: dict[str : str]
    """
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