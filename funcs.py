import requests
import sys
from constants import *
import writer
import testers


def get_friends(options: dict, friends_num_in_one_request=1000):
    """

    :param options: options got from get_options() function.
    :param friends_num_in_one_request: If memory limits are hard or very big data this param splits big request into
    several smaller ones.
    """
    method = "friends.get"
    report_path = options.pop("report_path")
    report_format = options.pop("report_format")
    file_name = options.pop("file_name")
    request_params = options.copy()
    request_params.update({"v": API_VK_VERSION})
    request_params.update({"fields": DEFAULT_FIELDS})

    friend_number_response = requests.get(API_MAIN_REF + "users.get",
                                          params={
                                              "v": API_VK_VERSION,
                                              "access_token": options['access_token'],
                                              "user_id": options['user_id'],
                                              "fields": "counters"
                                          }
                                          )
    friend_number = friend_number_response.json()['response'][0]['counters']['friends']
    request_params.update({"count": str(friends_num_in_one_request), "offset": 0, "order": "name"})
    writing = writer.write_to_file(report_path,
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
        writing = writer.write_to_file(report_path,
                                       REQUIRED_ATTRIBUTES,
                                       report_format=report_format,
                                       mode="w",
                                       head_or_tail="head")
    while request_params['offset'] < friend_number:
        response = requests.get(f"https://api.vk.com/method/{method}", params=request_params)
        error = testers.response_testing(response)
        if error:
            print(error)
            sys.exit(100)
        js_response = response.json()
        for user in js_response['response']['items']:
            while not writer.write_to_file(report_path, REQUIRED_ATTRIBUTES, user, report_format=report_format,
                                           mode="a") == "":
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
        request_params['offset'] = request_params['offset'] + friends_num_in_one_request
    writer.write_to_file(report_path,
                         REQUIRED_ATTRIBUTES,
                         user=None,
                         report_format=report_format,
                         mode="a",
                         head_or_tail="tail")
    if path.isfile(report_path):
        print("Report successfully saved to " + report_path)
    else:
        print("Report successfully saved to " + path.join(report_path, file_name))
