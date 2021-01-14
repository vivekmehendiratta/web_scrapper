from linkedin import Linkedin
import secrets
import time
import json

import college_urls
import notes

load=Linkedin(secrets.username, secrets.password, secrets.path_to_driver)
load.login()

# print(load.get_currentURL())

# profile_name = ''

# profileURL = load.search_profile(profile_name)

# load.search_people()

load.go_to_profile(profileURL=college_urls.gtech)

load.scroll_down()

profiles = load.get_all_profiles()
# print(profiles)


with open('profiles.json') as infile:
    resp_dict = json.load(infile)

j = 0
for profile in profiles:
    if profile not in resp_dict.keys():
        load.go_to_profile(profileURL=profile)
        res = load.connect_to_profile(note = notes.rest)
        if res == 'web driver exception':
            break
        resp_dict[profile] = res
    else:
        j+=1
        print(f'{profile} - already present {j}')

with open('profiles.json', 'w') as outfile:
    json.dump(resp_dict, outfile)
# print(resp_dict)

