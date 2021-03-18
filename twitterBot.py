import tweepy
import os

auth = tweepy.OAuthHandler(os.environ['consumer_key'], os.environ['consumer_secret_key'])
auth.set_access_token(os.environ['access_token'], os.environ['access_token_secret'])


api = tweepy.API(auth)

# public_tweets = api.home_timeline()
# for tweet in public_tweets:
#     print(tweet.user.name)    
#     print(tweet.user.screen_name)
#     print(tweet.text)
#     print(tweet.user.profile_image_url)
#     print(" ")
    

# kurtis_tweets = api.user_timeline(screen_name='kurtisconner', count=10)
# # print(tweets)

# for tweet in kurtis_tweets:
#     print(tweet.user.name)    
#     print(tweet.user.screen_name)
#     print(tweet.text)
#     print(tweet.user.profile_image_url)
#     print(" ")

atMentions = api.mentions_timeline()

# print(len(atMentions))
# print(atMentions.keys())
# this gets the text of a tweet
print(atMentions[0].text)


# api.update_status('hello world from @_gg_bot')
# print(api.mentions_timeline())