from bs4 import BeautifulSoup
import os, sys
import urllib2
#from urlparse import urlparse

#first line is label, subsequent lines have format <uri, ...>
inputFileName = 'URIs.txt'
masterOutputFileName = 'parentURIandChildrenLinks.txt'

timeoutValueInSeconds = 10
listOfItemsToSkip = []#2, 4

def extractLinkFromListOfURIs(listOfURIs, maximumNumberOfURIsToExplore = 100):

	if( len(listOfURIs) > 0 ):

		#for this parent URI
		dictionaryOfURIsWithLinks = {}

		try:
			masterOutputFile = open(masterOutputFileName, 'a')
		except:
			masterOutputFile.close()
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(fname, exc_tb.tb_lineno, sys.exc_info() )
			return

		for i in range(0, len(listOfURIs) ):

			uri = listOfURIs[i]

			if( i in listOfItemsToSkip ):
				print "...skipping, ",i, uri
				continue

			
			print "...item: ", i, ", total: ", len(dictionaryOfURIsWithLinks)

			if( len(dictionaryOfURIsWithLinks) >= maximumNumberOfURIsToExplore):
				masterOutputFile.close()
				print "entryCount > maximumNumberOfURIsToExplore"
				return

			try:
				if( timeoutValueInSeconds > 0 ):
					response = urllib2.urlopen(uri, timeout=timeoutValueInSeconds)
				else:
					response = urllib2.urlopen(uri)
			except:
				continue

			#restiction 1
			#print "...parent response code:", response.code
			if( response.code == 200 ):

				#parsedURI = urlparse(uri)
				try:
					parentURIfile = open('URI_LINKS_' + str(i) + '.txt', 'w')
				except:
					parentURIfile.close()
					continue

				parentURIfile.write(uri + '\n')
				masterOutputFile.write(uri + '\n')

				html = response.read()
				soup = BeautifulSoup(html)

				#extract all children URIs
				deleteIfFileEmptyFlag = True
				for link in soup.find_all('a'):
				    
				    potentialURI = link.get('href')
				    try:
				    	if( timeoutValueInSeconds > 0 ):
				    		response = urllib2.urlopen(potentialURI, timeout=timeoutValueInSeconds)
				    	else:
				    		response = urllib2.urlopen(potentialURI)
				    except:
				    	continue

				    #restiction 2
				    if( response.code == 200 ):

				    	#used to count parent URIs with children links
				    	dictionaryOfURIsWithLinks[uri] = ''

				    	parentURIfile.write('\t' + potentialURI + '\n')
				    	masterOutputFile.write('\t' + potentialURI + '\n')
				    	deleteIfFileEmptyFlag = False


				if( deleteIfFileEmptyFlag ):
					print "...removing: ", 'URI_LINKS_' + str(i) + '.txt'
					os.remove('URI_LINKS_' + str(i) + '.txt')

			parentURIfile.close()

		masterOutputFile.close()



def getInput():
	listOfURIs = []
	try:
		urlsFile = open(inputFileName)
		listOfURIs = urlsFile.readlines()
		urlsFile.close()
	except:
		urlsFile.close()
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		print(fname, exc_tb.tb_lineno, sys.exc_info() )
		return


	return listOfURIs

listOfURIs = getInput()
#listOfURIs = ['http://www.cs.odu.edu', 'http://www.ariesnonprofit.com']
extractLinkFromListOfURIs(listOfURIs, 1000)


