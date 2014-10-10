#Convert to dot file
...
outputFile.write('digraph ParentChildLinks {\n')
	listOfLabelsUncompressed = []
	if( len(lines) > 0 ):
		for uri in lines:
			#is this parent
			uri = uri.lower()
			if( uri[0] == 'h' ):
				#print "parent:", uri
				currentParent = uri.strip()
				listOfLabelsUncompressed.append(uri)
			else:
				#print "...child:", uri
				stringToWrite = '"' + currentParent.strip() + '" -> "' + uri.strip() + '"'
				outputFile.write(stringToWrite + '\n')
				listOfLabelsUncompressed.append(uri)

		labels = getCompressedURLName(listOfLabelsUncompressed)

		#label graphs
		if( len(labels) == len(listOfLabelsUncompressed) ):
			for i in range(0, len(listOfLabelsUncompressed)):
				outputFile.write('"'+ listOfLabelsUncompressed[i].strip() + '"' + ' [label="'+ labels[i].strip() +'"];' +'\n')

		outputFile.write('\n}')
		outputFile.close()
...