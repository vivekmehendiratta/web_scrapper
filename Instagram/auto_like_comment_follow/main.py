import secrets
import hashtags
from instapy import InstaPy

# login
session = InstaPy(username=secrets.username, password=secrets.password)
session.login()

# # Like posts based on hashtags
# session.like_by_tags(hashtags.hashtag_1, amount=20, randomize=True)

# # Comment
# session.set_do_comment(enabled=True, percentage=46)
# session.set_comments(hashtags.comments)


# #Like and Interact
# session.set_user_interact(amount=25, randomize=True, percentage=94, media='Photo')
# # session.like_by_tags(hashtags.hashtag_1, amount=10, interact=True)
# session.follow_by_tags(hashtags.hashtag_1, amount = 15, interact=True)



# set up all the settings
session.set_do_comment(True, percentage=75)
session.set_comments(hashtags.comments)
session.set_do_follow(enabled=True, percentage=60, times=2)
session.set_user_interact(amount=19, percentage=100, media='Photo')

# do the actual liking
session.like_by_tags(hashtags.hashtag_2, amount=10)

# end the bot session

session.end()

session.end()

