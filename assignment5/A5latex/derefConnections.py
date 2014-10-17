#Deference the count of connections for connections with 500+ connections
dictionaryOfConnectionsToDereference = get2ndDegreeConnectionsFromHTML(html)
...
#call function to get <friend, friendCount> and get ids of 500+ connection count to be dereferenced
if( len(dictionaryOfConnectionsToDereference) > 0 ):
	try:
		connectionsOutputFile = codecs.open(globalCSVOutputFile, 'a', 'utf-8')	
	except:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		print fname, exc_tb.tb_lineno, sys.exc_info()
		return
	count = len(dictionaryOfConnectionsToDereference)
	for connection, conElementID in dictionaryOfConnectionsToDereference.items():
		pleaseSleep()
		linkToGet = 'http://www.linkedin.com/profile/connections?id=' + conElementID
		myFirefoxBrowser.get(linkToGet)

		html = myFirefoxBrowser.page_source.encode('utf-8')
		connectionCount = getConnectionCountFor500PlusConnection(html)
		
		#append globalCSVOutputFile
		print "deref:", connection, connectionCount, count
		connectionsOutputFile.write( connection.decode('utf-8') + ', ' + connectionCount +'\n')
		count = count - 1
...