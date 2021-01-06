from linkedin import Linkedin
import creds
import time
import json

load=Linkedin(creds.username, creds.password, creds.path_to_driver)
load.login()

# print(load.get_currentURL())

# profile_name = 'McCombs School of Business, The University of Texas at Austin'

# profileURL = load.search_profile(profile_name)
load.go_to_profile(profileURL = "https://www.linkedin.com/school/theuniversityoftexasataustin-/people/")

# load.search_people()

load.scroll_down()

profiles = load.get_all_profiles()
# print(profiles)

note = """
I hope this message finds you in great health.

I will be joining MSBA program at the University of Texas at Austin this summer. I came across your profile and found it to be very interesting. It would be great if you consider connecting.

Best Regards,
Vivek Mehendiratta
"""

with open('profiles.json') as infile:
    resp_dict = json.load(infile)

for profile in profiles:
    if profile not in resp_dict.keys():
        load.go_to_profile(profileURL=profile)
        res = load.connect_to_profile(note = note)
        if res == 'web driver exception':
            break
        resp_dict[profile] = res
    else:
        print('already present')

with open('profiles.json', 'w') as outfile:
    json.dump(resp_dict, outfile)
# print(resp_dict)

