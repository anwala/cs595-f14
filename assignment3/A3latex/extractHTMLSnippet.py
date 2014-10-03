#Extract HTML function
def extractHTMLAndSave():

	if( len(uriHashDictionary) > 0 ):
		count = 0
		for uri in uriHashDictionary:

			filename =  str(count) + '-' + uriHashDictionary[uri] + '.html'
			co = 'curl -s -L ' + uri + ' > ./RawHtml/' + filename
			
			commands.getoutput(co)
			count = count + 1