from instagram.client import InstagramAPI

access_token = "2089831609.1fb234f.6499c31f18ab4126abd00b8f833970dd"
# client_secret = "7d816b67712d4624988fe2c7b3a545d8"
client_secret = ""

# user_id = "dsi430d"

relations = {}
depth_max = 2
f = open('pageRank_instagram.txt','w')

api = InstagramAPI(access_token=access_token)

def user_follows(person_id, depth):
    max = 0
    if person_id in relations:
        return 0
    else:
        relations[str(person_id)] = []
    try:
        for user in api.user_follows(person_id)[0]:
            max = max + 1
            if max >=40:
                return  0
            f.write(str(person_id)+" -neighbor- "+str(user.id)+"\n")
            # relations[str(person_id)].append(str(user.id))
            if depth<=depth_max:
                user_follows(user.id, depth+1)
    except:
        return 0


influencers = ['ChiaraFerragni','songofstyle','juliahengel','tuulavintage','susiebubble','peaceloveshea','zoella','laurenconrad','marianodivaio','audrinapatridge','whowhatwear']
for inf in influencers:
    try:
        user_follows(api.user_search(inf)[0].id,0)
    except:
        continue


# original test
# user_follows(1725181484,0)
# print api.user_search('ChiaraFerragni')[0].id


f.close()


