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

globalDelimeter = ' ,, '
globalDelimeter2 = ' -> '

def getPlusCountAndTabCount(inputString):

	tabCount = 0
	plusCount = 0

	if( len(inputString) > 0 ):
		for i in range(0, len(inputString)):

			if( inputString[i] == '\t' ):
				tabCount += 1
			elif( inputString[i] == '+'):
				plusCount += 1


	return plusCount, tabCount,

def getMultiDegreeFriends(screenName, userName, maxFriends, maxDegree, outputFileName):

	if( maxFriends > 0 and maxDegree > -1 and len(userName) > 0 and len(screenName) > 0 and len(outputFileName) > 0 ):

		try:
			inputOutputFile = open(outputFileName, 'r+')
		except:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(fname, exc_tb.tb_lineno, sys.exc_info() )
			return

		lines = inputOutputFile.readlines()
		

		if( len(lines) == 0 ):
	
			#base case initialize with 1 degree+
			friends = getXFriendsOfFriendsFromTwitter(screenName, maxFriends)

			for friend in friends:
				inputOutputFile.write(userName + globalDelimeter2 + friend + '+\n' )

		else:

			#non-base case expand item with smallest plus within tabcount
			mininumPlus = 1000
			item = ''
			itemTabCount = 0
			indexOfItem = -1

			i = 0
			for line in lines:

				plusCount, tabCount = getPlusCountAndTabCount(line)

				#print line.strip(), plusCount, tabCount
				#get minimum plus count which is within the set degree
				if( plusCount != 0 and plusCount < maxDegree ):
					if( plusCount < mininumPlus and tabCount < maxDegree ):
						mininumPlus = plusCount
						item = line
						itemTabCount = tabCount
						indexOfItem = i

				i += 1
					
			
			#print item.strip(), itemTabCount, indexOfItem


			if( indexOfItem > -1 ):
				inputOutputFile.close()

				#expand
				try:
					inputOutputFile = open(outputFileName, 'w')
				except:
					exc_type, exc_obj, exc_tb = sys.exc_info()
					fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
					print(fname, exc_tb.tb_lineno, sys.exc_info() )
					return
				
				for i in range(0, len(lines)):

					if(i == indexOfItem):

						tabs = str('\t') * itemTabCount
						inputOutputFile.write(tabs + lines[i].strip() + '+\n')


						screenName = lines[i].strip()
						screenName = screenName.split(globalDelimeter)[1]
						screenName = screenName.replace('+','')

						#get userName
						userName = lines[i].strip()
						userName = userName.split(globalDelimeter)[0]
						userName = userName.split(globalDelimeter2)
						userName = userName[-1]

					
						friends = getXFriendsOfFriendsFromTwitter(screenName, maxFriends)

						for friend in friends:

							tabs = str('\t') * (itemTabCount+1)
							inputOutputFile.write( tabs + userName + globalDelimeter2 + friend + '+\n' )
					else:
						inputOutputFile.write(lines[i])


		inputOutputFile.close()

		if(indexOfItem == -1):
			sys.exit()

def getXFriendsOfFriendsFromTwitter(screenName, countOfFriends):


	listOfFriendsScreeNames = []
	if( len(screenName) > 0  and countOfFriends > 0):

		#requestsRemaining = api.rate_limit_status()['resources']['search']['/search/tweets']['remaining']
		requestsRemaining = api.rate_limit_status()['resources']['friends']['/friends/list']['remaining']
		print "Before Request remaining: ", requestsRemaining

		while( len(listOfFriendsScreeNames) < countOfFriends ):

			try:
				friends = api.friends(screen_name=screenName, count=countOfFriends)
			except:
				friends = []
				print 'error,', screenName
				exc_type, exc_obj, exc_tb = sys.exc_info()
				fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
				print fname, exc_tb.tb_lineno, sys.exc_info()

			if( len(friends) == 0 or len(friends) > countOfFriends):
				break

			for friend in friends:
				screenNameUserNameTuple = friend.name + globalDelimeter + friend.screen_name
				screenNameUserNameTuple = screenNameUserNameTuple.encode('ascii', 'ignore')
				listOfFriendsScreeNames.append(screenNameUserNameTuple)

		    

		    #time.sleep(31)

		requestsRemaining = api.rate_limit_status()['resources']['friends']['/friends/list']['remaining']
		print "After Request remaining: ", requestsRemaining

	return listOfFriendsScreeNames


screenName = 'phonedude_mln'
userName = 'Dr. Nelson'
#<screen_name, maximumFriends, maximumDegree, outputFile>
getMultiDegreeFriends(screenName, userName, 3, 4, 'multiDegreeFriends.txt')