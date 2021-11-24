import sys
import getters
from time import time
import funcs

if __name__ == "__main__":
    options = getters.get_options()
    funcs.get_friends(options, friends_num_in_one_request=1000)

