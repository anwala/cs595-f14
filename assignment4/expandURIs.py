import os, sys
import requests

#Expand url
def followTheRedirectCurl(url):
	if(len(url) > 0):
		try:
			r = requests.head(url, allow_redirects=True)
			return r.url
		except:
			return url
	else:
		return url



def expandURIS():

	inputFile = open('parentURIandChildrenLinks.txt', 'r')
	outputFile = open('ExpandedparentURIandChildrenLinks.txt', 'w')
	unexpandedURIs = inputFile.readlines()
	inputFile.close()

	for uri in unexpandedURIs:

		#parent
		if( uri[0] == 'h' ):
			expandedURI = followTheRedirectCurl(uri.strip())
			outputFile.write(expandedURI + '\n')
		else:
			expandedURI = followTheRedirectCurl(uri.strip())
			outputFile.write('\t' + expandedURI + '\n')


	outputFile.close()


expandURIS()
