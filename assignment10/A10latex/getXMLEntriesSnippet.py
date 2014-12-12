#get blog entries
'''
	input:
		blogUrl:
			'http://blogNameHere.blogspot.com/'
		outputXMLFileName:
			'blogEntries.xml'
'''
def getXMLEntriesFromBlog(blogUrl, outputXMLFileName, maximumEntries=10):

	if( len(blogUrl) > 0 and len(outputXMLFileName) > 0 and maximumEntries > 0 ):
		maximumEntries = str(maximumEntries)
		blogUrl = blogUrl.strip()
		try:
			co = 'curl -s ' + blogUrl + 'feeds/posts/default?max-results='+maximumEntries
			output = commands.getoutput(co)

			outputFile = open(outputXMLFileName, 'w')
			outputFile.write(output)
			outputFile.close()
		except:
			print 'Failed to parse feed %s' % blogUrl
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(fname, exc_tb.tb_lineno, sys.exc_info() )