This app is created to get friends list for required user.


To run the application you need an installed python interpreter.
Also some not standart libraries are required:
1) requests


On start it requires few params:
1) User access_token (Instruction how to get it is given below)
2) User id - is integer number of user profile id whose friends list to request. User profile mustn't be private, deleted or banned. 
Anyway if requested user profile is private,
deleted or banned, program will report and ask for valid user id.
3) Report format. Now three formats are implemented to give report in: csv(Comma Separated Values), tsv(Tabulate Separated Values)
and json(JavaScript Object Notation). Just type on of them.
4) Path to report. Directory where to save the report.


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
Press "Allow" and copy long sequence of digits and characters between "access_token=" and "&expires_in"
This is your user access token. Note its lifetime usually is 24 hours(86400 seconds) from request time.
Note: I am not related with this apps and don't know how do they aggregate issued permissions.