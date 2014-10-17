import tweepy
import os, sys
import time

# Consumer keys and access tokens, used for OAuth
consumer_key = 'DzOQzhefR1KUZU6o9K3KpUGe8'
consumer_secret = 'ywrRDh364xyCsihVcGP5KhgJAAC5qYgDWCwTO6y6PlK4nZSZct'
access_token = '2592291038-McunBCHwoIDi7u7ehUSgtSyQmQTfIIBIhVNo14F'
access_token_secret = 'IjkHA5yDn3UdHeGWaRNr3epJYNGTvYOHMCayYv2lLoQ4V'

# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Creation of the actual interface, using authentication
api = tweepy.API(auth)


def getFriendsOfFriendsFromTwitter(screenName):
	if( len(screenName) > 0 ):


		try:
			friendCountFile = open('friendsCountFile.csv', 'w')
		except:
			 exc_type, exc_obj, exc_tb = sys.exc_info()
			 fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			 print(fname, exc_tb.tb_lineno, sys.exc_info() )

		#requestsRemaining = api.rate_limit_status()['resources']['search']['/search/tweets']['remaining']
		requestsRemaining = api.rate_limit_status()['resources']['friends']['/friends/list']['remaining']
		print "Before Request remaining: ", requestsRemaining
		
		

		user = api.get_user(screenName)

		friendsCount = str(user._json['friends_count'])
		print screenName + ' has ' + friendsCount + ' friends, and '

		friendCountFile.write('"USER", "FRIENDCOUNT"\n')
		friendCountFile.write(user.name.encode('utf-8') + ', ' + friendsCount + '\n')

		for friend in user.friends(count=int(friendsCount)):
			friendsCount = str(api.get_user(friend.screen_name).friends_count)
			print friend.name + ' has ' + friendsCount + ' friends'

			
			friendCountFile.write(friend.name.encode('utf-8') + ', ' + friendsCount + '\n')



		requestsRemaining = api.rate_limit_status()['resources']['friends']['/friends/list']['remaining']
		print "After Request remaining: ", requestsRemaining


		friendCountFile.close()



		


#screenName = 'phonedude_mln'
#screenName = 'acnwala'
#getFriendsOfFriendsFromTwitter(screenName)


