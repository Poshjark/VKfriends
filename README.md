This app is created to get friends list for required user.

For users
To run the application you need an installed python interpreter.
Before first execution, after python interpreter reinstalling or after changing virtual enviroment (python venv) run following command in your command line(windows) / terminal(linux):
pip install -r requirements.txt

On start it requires few params:
1) User access_token (Instruction how to get it is given below)
2) User id - is integer number of user profile id whose friends list to request. User profile mustn't be private, deleted or banned. 
Anyway if requested user profile is private, deleted or banned, program will report and ask for valid user id.
3) Report format. Now three formats are implemented to give report in: csv(Comma Separated Values), tsv(Tabulate Separated Values)
and json(JavaScript Object Notation). Just type on of them. Default  - csv
4) Path to report. Directory where to save the report. Default - work directory where scripts is called from.


How to get user access token.
There are two similar ways:
1) Copy and paste to address bar of your internet browser following link - 
https://oauth.vk.com/authorize?client_id=8009316&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=friends&response_type=token&v=5.131

Press "Allow" and copy long sequence of digits and characters between "access_token=" and "&expires_in"
This is your user access token. Note its lifetime usually is 24 hours(86400 seconds) from request time.
This app is created just to give tokens and it doesn't save, doesn't aggregate and doesn't give your personal information including token to anyone.

2) Similar way. Copy and paste to address bar of your internet browser following link - 
https://vkhost.github.io/

Choose one of represented apps and click its button.
Press "Allow"/"Разрешить" and copy long sequence of digits and characters between "access_token=" and "&expires_in"
This is your user access token. Note its lifetime usually is 24 hours(86400 seconds) from request time.
Note: I am not related with this apps and don't know how do they aggregate issued permissions.

For developers.
How it works:
Firstly script requests input data: access_token, user_id, report_format and report_path. Each parameter is requested from user by its own getter(from getters.py) where this option is being checked too with specific rules.
For example user_id must be integer and this profile mustn't be private or deactivated. 
Then this options are passed to get_friends() function. 
This function process these options and requests friends list from VK API. 
In cases when you expect big large amount of data just edit default friends_num_in_one_request param to convinient number. According to its name this param define how much users will be requested at one time.
After request main loop of function starts. There users are being written to report file from response. Then new request is being created. And so again till the end of friends list.
Users are being written to report file one by one so we need to format each user data to required format. For each implemented format in formatters.py there are dict FORMATS with formatting rules. E.g. separators between options or necessity of writing keys in the beginning. Also there are reference to formatter for this format that actually formats user data to string representation.
When writing is over succesfully script prints message that report was successfully written and where is report.

If you want to add new format you will need to implement its formatter and add required information to FORMATS dict from formatters.py implmenting all its keys.
If your format is similar with csv or tsv you can copy one of these formats in FORMATS editing "options_separator" value.
