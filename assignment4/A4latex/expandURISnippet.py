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