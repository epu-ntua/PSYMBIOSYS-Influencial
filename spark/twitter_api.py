import twitter
import time

api = twitter.Api(consumer_key='GDWyb1WBb0yJwYBwQ9g3m2nFx',
                      consumer_secret='BK78W93LakpOwPL84otIl2dVZQ0gNjAYPiFWQbCfdFO6UiF0lF',
                      access_token_key='95257276-aptBPzbJCDqJWKKZ65RwgtJehNiOTEgoyASzaIPqQ',
                      access_token_secret='0qHtIAuQSHUXEeTZ5AHwc8SJaHULyJcPyhEdc5QI5bF1I')

def member_metric(member):
    tweets =  api.GetUserTimeline(user_id =member.id)
    mentions = 0
    for tweet in tweets:
        mentions =  mentions + tweet.retweet_count
    if tweets > 0:
        return (mentions*1.0)/len(tweets)
    else:
        return 0

def profile(member):


    member = api.GetUser(screen_name=member)

    url = member.url
    description = member.description
    id = member.id
    # metric =  member_metric(member)
    metric = 0
    # TODO improve the call to start from the last tweet
    last_tweet_id = None
    # time.sleep(10)
    return {
        "metric":metric,
        "full_name":member.name,
        "profile_image_url":str(member.profile_image_url).replace("_normal","")
    }



# print profile("apilama")

