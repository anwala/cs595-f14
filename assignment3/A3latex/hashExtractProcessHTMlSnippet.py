#3 functions to hash URIs, extract HTML and process HTML 
def getHashFromURI(uri):

	md5hash = ''

	if( len(uri) > 0 ):
		# Assumes the default UTF-8; http://www.pythoncentral.io/hashing-strings-with-python/
		hash_object = hashlib.md5(uri.encode())
		md5hash = hash_object.hexdigest()

	return md5hash

def extractHTMLAndSave():

	if( len(uriHashDictionary) > 0 ):
		count = 0
		for uri in uriHashDictionary:

			filename =  str(count) + '-' + uriHashDictionary[uri] + '.html'
			co = 'curl -s -L ' + uri + ' > ./RawHtml/' + filename
			
			commands.getoutput(co)
			count = count + 1

def processHTMLAndSave():

	if( len(uriHashDictionary) > 0 ):

		count = 0

		for uri in uriHashDictionary:
			
			filename = str(count) + '-' + uriHashDictionary[uri] + '.html'
			count = count + 1

			try:
				co = 'lynx -dump -force_html ' + uri
				processedFileText = commands.getoutput(co)

				outputHtmlFile = open('./ProcessedHtml/processed_' + filename, 'w')
				outputHtmlFile.write(processedFileText)
				outputHtmlFile.close()

			except:
				exc_type, exc_obj, exc_tb = sys.exc_info()
				fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
				print(fname, exc_tb.tb_lineno, sys.exc_info() )
				return