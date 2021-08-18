from linkedin import Linkedin
import secrets
import time
import json

import college_urls
import company_urls
import notes


def connectWithNewProfiles(load, url, connection_note, scroll_counter, json_file):

    with open(json_file) as infile:
        try:
            resp_dict = json.load(infile)
        except Exception:
            pass

    load.go_to_profile(profileURL=url)

    load.scroll_down(scroll_counter)

    profiles = load.get_all_profiles()
    print(f'{len(profiles)} profiles found')
    j = 0
    for profile in profiles:
        if profile not in resp_dict.keys():
            load.go_to_profile(profileURL=profile)
            res_check = load.checkConnection()

            if (res_check == 'pending') or (res_check == 'connected'):
                resp_dict[profile] = 'success'
            elif (res_check == 'locked') or (res_check == 'follow'):
                resp_dict[profile] = 'fail'
            elif res_check == 'connect':
                res = load.connect_to_profile(note=connection_note)

                if res == 'web driver exception':
                    break

                if res != 'success':
                    print(f'FAILED to connect with {profile}')

                resp_dict[profile] = res
        else:
            j += 1
            print(f'{profile} - already present {j}')

    with open(json_file, 'w') as outfile:
        json.dump(resp_dict, outfile)

    load.end_session()
    print('session ended')
    return


def connectWithProfileList(connection_note, profiles_file_name):
    load = Linkedin(secrets.username, secrets.password, secrets.path_to_driver)
    load.login()

    with open(profiles_file_name) as infile:
        resp_dict = json.load(infile)

    for k, v in resp_dict.items():
        profile = k
        if v == 'fail':
            load.go_to_profile(profileURL=profile)
            res = load.checkConnection()
            if res:
                resp_dict[profile] = 'success'
            if res == False:
                res = load.connect_to_profile(note=connection_note)

                print(res)
                if res == 'web driver exception':
                    break

                if res != 'success':
                    print(f'FAILED to connect with {profile}')

                resp_dict[profile] = res

        with open(profiles_file_name, 'w') as outfile:
            json.dump(resp_dict, outfile)

    load.end_session()
    print('session ended')

    return


def createProfilesDB(load, urls, scroll_counter, json_file):
    with open(json_file) as infile:
        try:
            resp_dict = json.load(infile)
        except Exception:
            pass
    
    for organization_url in urls:
        print(organization_url)
        load.go_to_profile(profileURL=organization_url)

        load.scroll_down(scroll_counter)

        profiles = load.get_all_profiles()
        
        print(f'{len(profiles)} profiles found')

        j = 0
        for profile in profiles:

            if profile not in resp_dict.keys():
                resp_dict[profile] = 'not connected'
            else:
                j += 1
                print(f'{profile} - already present {j}')


        with open(json_file, 'w') as outfile:
            json.dump(resp_dict, outfile)

    load.end_session()
    print('session ended')

    return


connectWithProfileList(connection_note = notes.rest_updated, profiles_file_name='profiles_db.json')

### Use this code for testing ##################
# load=Linkedin(secrets.username, secrets.password, secrets.path_to_driver)
# load.login()
# time.sleep(5)
# load.go_to_profile(profileURL="https://www.linkedin.com/in/brian-payne-3a74391/")
# time.sleep(5)
# res = load.checkConnection()
# print(res)
######################################################


# urls = [
#     company_urls.alphabet,
#     company_urls.exxonmobil,
#     company_urls.twitter,
#     company_urls.mck_comp,
#     company_urls.bain_comp,
#     company_urls.two_sigma,
#     company_urls.akuna_capital
# ]

# load = Linkedin(secrets.username, secrets.password, secrets.path_to_driver)
# load.login()
# createProfilesDB(load=load,
#                  urls=urls,
#                  scroll_counter=50,
#                  json_file='profiles_db.json')
