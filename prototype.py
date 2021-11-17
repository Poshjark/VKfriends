import requests
import json
METHOD =            "friends.get"
METHOD_1 = "users.get"
TOKEN = ""
MY_TOKEN =  ""
V = "5.131"
user_id = 239468586
my_user_id = 50627330
fields = "name,country,city,birthdate,sex"
lang = 0
# first_name, surname, country, city, birthdate, sex

request = f"https://api.vk.com/method/friends.get?user_id={user_id}&lang={lang}&fields={fields}&access_token={MY_TOKEN}&v={V}"
print(request)
response = requests.get(request)
js_response = response.json()
print(js_response)
attributes_needed = ("first_name","last_name", "country", "city", "bdate", "sex")
attributes_with_options = {"country" : "title", "city" : "title"}
for user in js_response['response']['items']:

    for key in attributes_needed:
        print(key, " - ", end="")
        try:
            user[key]
            if key in attributes_with_options.keys():
                result = str(user[key][attributes_with_options[key]]) + '\t'
            else:
                if key == "sex":
                    sex = "Муж" if user[key] == 1 else "Жен"
                    result = sex + '\t'
                else:
                    result = str(user[key]) + '\t'
            print(result,end = "\t")
        except KeyError:
            print("No data", end = '\t')
    print()