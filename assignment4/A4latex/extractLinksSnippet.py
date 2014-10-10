#extract all children URIs
...
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
...