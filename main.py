import sys
from funcs import *






def main():
    method = "friends.get"
    options = get_options()
    request_params = options.copy()
    print(options)
    options.pop("report_path")
    options.pop("report_format")
    options.update({"v" : "5.131"})
    options.update({"fields":DEFAULT_FIELDS})
    response = requests.get(f"https://api.vk.com/method/{method}",params=options)
    error = response_testing(response)
    if error:
        print(error)
        sys.exit(100)
    js_response = response.json()
    while not write_to_file(REQUIRED_ATTRIBUTES, mode="w") == "":
        print("Please close file and type 'continue' to try to continue writing or type 'exit' to abort ")
        test = input()
        if test == "continue":
            continue
        else:
            while test != "continue":
                print("Type 'continue' to try to continue writing or type 'exit' to abort ")
                test = input()
                if test == "exit":
                    sys.exit(1)
    for user in js_response['response']['items']:
        while not write_to_file(REQUIRED_ATTRIBUTES, user, mode="a") == "":
            print("Please close file and type 'continue' to continue writing")
            test = input()
            if test == "continue":
                continue
            else:
                while test != "continue":
                    print("Type 'continue' to try to continue writing or type 'exit' to abort ")
                    test = input()
                    if test == "exit":
                        sys.exit(1)
    print()


if __name__ == "__main__":
    main()