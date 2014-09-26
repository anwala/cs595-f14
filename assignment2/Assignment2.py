import tweepy

import calendar
import time
import datetime

import os, sys

import threading

#from urlparse import urlparse
import requests

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

globalListOfUrls = []

globalUrlsFileName = 'linksFile.txt'
sinceIDFilename = 'tweetSinceIDFile.txt'
globalLengthOfLinksFile = 0


def followTheRedirectCurl(url):
	if(len(url) > 0):

		try:
			r = requests.head(url, allow_redirects=True)
			return r.url
		except:
			return ''
	else:

		return ''
		
def getUrisArray(potentialUrls):

	expandedUrlsList = []
	if(len(potentialUrls) > 0):

		for u in potentialUrls:

			url = (u['expanded_url'])
			#url = urlparse(url)
			#url = url.scheme + '://' + url.netloc
			url = followTheRedirectCurl(url)

			expandedUrlsList.append(url)

	return expandedUrlsList

def isInsideList(listOfItems, url):
	if(len(listOfItems) > 0 and len(url)> 0):

		for u in listOfItems:
			if(u.lower().strip() == url.lower().strip()):
				return True

	return False

def fetchResultsFromTwitter(searchQuery='www%2E-filter:link', numberOfPullRequestsToInitiate=1, sinceIDValue = 0):

	if( len(searchQuery) < 1 or numberOfPullRequestsToInitiate < 1):
		return

	requestsRemaining = api.rate_limit_status()['resources']['search']['/search/tweets']['remaining']
	#requestsRemaining = 10
	print "Before Request remaining: ", requestsRemaining

	if( requestsRemaining >= numberOfPullRequestsToInitiate ):

		try:
			urlsDataFile = open(globalUrlsFileName, "a+")
			urlsDataFileLongString = urlsDataFile.readlines()

			if(sinceIDValue == 0):
				sinceIDFile = open(sinceIDFilename, 'r')
				line = sinceIDFile.readline()
				sinceIDFile.close()

				if(len(line) > 0):
					line = line.split(',')[0].strip()
					sinceIDValue = long(line)

			
		except:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(fname, exc_tb.tb_lineno, sys.exc_info() )

			urlsDataFile.close()

			if(sinceIDValue == 0):
				sinceIDFile.close()
			return


		modifiedUrlsDataFileLongString = []
		
		for l in urlsDataFileLongString:
			#project only urls
			modifiedUrlsDataFileLongString.append(l.split(',')[0].lower().strip())


		#print modifiedUrlsDataFileLongString
		
		#make numberOfPullRequests request to twitter
		for i in range(0, numberOfPullRequestsToInitiate):

			#get tweets newer than sinceIDValue
			#print "...if: getting tweets newer than since_id"
			#print "...since_value: ", sinceIDValue

			#for tweet in tweepy.Cursor(api.search, q=searchQuery).items():
			#for tweet in tweepy.Cursor(api.search, q=searchQuery, since="2014-01-01",until="2014-09-19").items(15):
			#for tweet in tweepy.Cursor(api.search, q=searchQuery, since_id=long(sinceIDValue)).items(15):
			for tweet in tweepy.Cursor(api.search, q=searchQuery).items(30):

				
				#print tweet.id, tweet.created_at
				if( tweet.id > sinceIDValue ):
					sinceIDValue = tweet.id

				expandedUrlsList = getUrisArray(tweet.entities['urls'])

				if(len(expandedUrlsList) > 0):
					for u in expandedUrlsList:

						if(len(u) > 0):
							u = u.lower().strip()

							#if u not in modifiedUrlsDataFileLongString:
							if isInsideList(modifiedUrlsDataFileLongString, u) == False:
								print "...adding: ", u
								urlsDataFile.write( u + ', ' + str(tweet.id) + ', ' + str(datetime.datetime.now()) + '\n' )
								modifiedUrlsDataFileLongString.append(u)
							#else:
								#print "...inside already: ", u


	return len(modifiedUrlsDataFileLongString)



	#write a new since_id
	try:
		sinceIDFile = open(sinceIDFilename, 'w')
		sinceIDFile.write(str(sinceIDValue) + ', ' + str(datetime.datetime.now()) + '\n' )
		sinceIDFile.close()
	except:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		print(fname, exc_tb.tb_lineno, sys.exc_info() )

		sinceIDFile.close()
		return

	urlsDataFile.close()


#queries
#http:// - http%3A%2F%2F
#http://www. - http%3A%2F%2Fwww%2E-filter:link
#www. - www%2E

#http://www. -filter:link; only tweets with links
#fetchResultsFromTwitter(searchQuery='www%2E-filter:link', numberOfPullRequestsToInitiate=1, sinceIDValue=0)

lengthOfLinksFile = 0
while(lengthOfLinksFile < 1500):
	lengthOfLinksFile = fetchResultsFromTwitter(searchQuery='www%2E-filter:link', numberOfPullRequestsToInitiate=1, sinceIDValue=0)
	print "...lengthOfLinksFile: ", lengthOfLinksFile
	time.sleep(15)


'''
https://dev.twitter.com/rest/public/rate-limiting
https://dev.twitter.com/rest/public/timelines
https://dev.twitter.com/rest/reference/get/search/tweets
https://dev.twitter.com/rest/public/search
https://media.readthedocs.org/pdf/tweepy/v2.3.0/tweepy.pdf
def Recyclebin():

	#m=512426969653592065
	#s=512426973378134016

	def unshortenUrl_old(url):

	if(len(url) > 0):
		try:
			response = urllib2.urlopen(url)
			return response.url
		except:
			return url
	else:
		return url


	#Get the number of remaining requests
	#rate_info = api.rate_limit_status()['resources']['search']
	#rate_info = api.rate_limit_status()['resources']['search']['/search/tweets']['reset']

	#rate_info = api.rate_limit_status()['resources']['search']['/search/tweets']
	#print rate_info



	#searchRateLimitValue = api.rate_limit_status()['resources']['search']['/search/tweets']['limit']
	#numberOfRequestPerMinute = (searchRateLimitValue - 10)/15
	#print type(searchRateLimitValue)


	#now = time.time()
	#future = now + 10
	#while time.time() < future:
	    # do stuff
	#    print datetime.datetime.now()
	#    pass

	#rate_info = api.rate_limit_status()['resources']['application']['/application/rate_limit_status']
	#print rate_info
	#print ""

	#for tweet in tweepy.Cursor(api.search, q='t.co', count=1, lang="en").items():
	#	print tweet.text
	#	print ""

	#rate_info = api.rate_limit_status()['resources']['search']
	#print rate_info
	#print ""

	#cur_time = rate_info
	#cur_time = calendar.timegm(datetime.datetime.utcnow().timetuple())
	#cur_time = datetime.datetime.utcnow().timetuple()

	#normalTime = time.localtime(cur_time)
	#normalTime = time.localtime(1410922857)
	#print str(normalTime.tm_mon) + ':' + str(normalTime.tm_mday) + ':' + str(normalTime.tm_year)
	#print str(normalTime.tm_hour) + ':' + str(normalTime.tm_min) + ':' + str(normalTime.tm_sec)



	#for url in globalListOfUrls:
	#	print '	', url
				



	#rate limit: request count is based on page

	#based upon https://dev.twitter.com/rest/public/timelines, but doesn't work 
	def fetchResultsFromTwitter_old(searchQuery, maximumItems = 15):

		tweetMaxID = 0
		tweetSinceID = 0

		try:
			maxIDSinceIDFile = open('tweetMaxIDAndSinceIDFile.txt', 'r')
			lines = maxIDSinceIDFile.readlines()
			maxIDSinceIDFile.close()

			if(len(lines) > 0):
				tweetMaxID = long(lines[0])
				tweetSinceID = long(lines[1])


		except:
			maxIDSinceIDFile.close()


		count = 1
		if( tweetMaxID > 0 and tweetSinceID > 0 ):
			print "if"
			print ""
			for tweet in tweepy.Cursor(api.search, q=searchQuery, lang="en",since_id=tweetSinceID, max_id=tweetMaxID-1).items(maximumItems):

				if(tweet.id < tweetMaxID):
					tweetMaxID = tweet.id

				if(tweet.id > tweetSinceID):
					tweetSinceID = tweet.id

				print "id: ", tweet.id
		else:
			print "else"
			print ""
			for tweet in tweepy.Cursor(api.search, q=searchQuery, lang="en").items(maximumItems):

				if( count == 1 ):
					tweetMaxID = tweet.id

				if(tweet.id < tweetMaxID):
					tweetMaxID = tweet.id

				if(tweet.id > tweetSinceID):
					tweetSinceID = tweet.id

				count = count + 1

				print "id: ", tweet.id
				


		try:
			maxIDSinceIDFile = open('tweetMaxIDAndSinceIDFile.txt', 'w')
			maxIDSinceIDFile.write(str(tweetMaxID) + '\n')
			maxIDSinceIDFile.write(str(tweetSinceID) + '\n')
			maxIDSinceIDFile.close()
		except:
			maxIDSinceIDFile.close()



		#count = 1
		#for tweet in tweepy.Cursor(api.search, q=searchQuery, lang="en").items(15):





		#	print count
		#	count = count + 1



		#count = 1
		#for page in tweepy.Cursor(api.search, q=searchQuery, lang="en").pages(pageMax):
		#	for tweet in page:
		#		print count
		#		count = count + 1

	def searchTwitterForUris_old(searchQuery, maximumItemsCount = 1000):

		urlsDateFile = open(globalUrlsFileName, "a")
		if( len(searchQuery) > 0 ):

			itemsCount = 0

			#for tweet in tweepy.Cursor(api.search, q=searchQuery, count=2000, lang="en").items():
			for tweet in tweepy.Cursor(api.search, q=searchQuery, count=100).items():
				itemsCount = itemsCount + 1

				if( len(globalListOfUrls) == maximumItemsCount ):
					break

				potentialUrls = tweet.entities['urls']
				if(len(potentialUrls) > 0):

					for u in potentialUrls:
						url = urlparse(u['expanded_url'].lower())

						if( url.netloc not in globalListOfUrls ):
							uri = url.netloc
							globalListOfUrls.append(uri)
							urlsDateFile.write(uri + '\n')
							print uri

				if(itemsCount >= 11):
					itemsCount = 0
					urlsDateFile.write('\n')
					time.sleep(60)



		urlsDateFile.close()
'''