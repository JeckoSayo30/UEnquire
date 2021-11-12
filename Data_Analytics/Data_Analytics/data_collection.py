import tweepy
import json

# TWITTER ACCOUNT ACCESS
secret = []
file = open("../secret.txt", "r")
for line in file:
	secret.append(line.rstrip())	
file.close() 

consumer_key = secret [0]
consumer_secret = secret[1]
access_token = secret[2]
access_token_secret = secret[3]

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token,access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit_notify=True, wait_on_rate_limit=True)

num_post = 177
# 2478

accts = [
	'@UnivEast','@theweeklydawn','@UEUSC_Official', '@RWconnects',
	'@ueccss_sc','@UE_DSC', '@uemanila_cassc', '@uepssofficial',
	'@uemnl_cbasc', '@uejournsoc', '@UEPsychSoc', '@uebroadcasting',
	'@ueceducofficial', '@UESHSSC'
]

posts = []
sources = []

for i in accts: 
	# print(1)
	sources.append(tweepy.Cursor(api.user_timeline, id = i, tweet_mode = "extended").items(num_post))

for post in sources:
	for i in post:
		posts.append(i.full_text)
		# print(i.full_text)
		print("LOADING, length: ", len(posts))


raw_data = {'tweets': posts}
# print(posts)
print("Length: ", len(posts))
with open("dataset.json", 'w') as data_file:
	json.dump(raw_data, data_file, indent=4)