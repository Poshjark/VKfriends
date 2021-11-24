from requests import Response
from constants import *


def response_testing(response: Response) -> str:
    """
    Tests if response has errors. If it has returns error from ERROR_CODES dict from constants.
    :param response: result of requests.get(url)
    :return: If no errors returns empty string. Else returns error message.
    """
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