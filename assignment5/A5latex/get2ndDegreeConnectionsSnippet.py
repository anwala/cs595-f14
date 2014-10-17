#write <connection, connectionCount> tuples into globalCSVOutputFile
#returns connection element ids of connections with 500+ connections to be dereferenced
def get2ndDegreeConnectionsFromHTML(connectionsHtml):
...
indexOfConnection = 0
for connection in allConnections:

	person = connection.find('input', { 'type' : 'checkbox' })
	#person is of form: <input type="checkbox" value="Marc Abramo Serr"/>

	if( person is not None ):
		person = str(person)
		connectionName = person.split('"')

		#get connection count, name is 3rd position
		if( len(connectionName) > 2 ):
			
			connectionCount = connection.find('div', { 'class' : 'conn-count' })
			connectionCount = connectionCount.text

			#get id
			idOfElement = str(connection)
			indexIdOfElement = idOfElement.find('id="')

			if( indexIdOfElement > -1 ):
				indexIdOfElement = indexIdOfElement + 4
				indexIdOfElementClosingQuotes =	idOfElement.find('"', indexIdOfElement)
				connectionHTMLElementID = idOfElement[indexIdOfElement : indexIdOfElementClosingQuotes]
				
				#print connectionName[3], connectionCount, connectionHTMLElementID + '\n'
				connectionCount = connectionCount.strip()
				if( connectionCount == '500+' ):
					dictionaryOfConnectionsToDereference[connectionName[3]] = connectionHTMLElementID
				else:
					connectionsOutputFile.write( connectionName[3].decode('utf-8') + ', ' + connectionCount +'\n')
...