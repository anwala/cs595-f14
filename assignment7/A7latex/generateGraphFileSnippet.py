#Generate graph file
...
i = 0
for relationship in relationships:
	sourceAndTarget = relationship.split(' ,, ')[0]
	source = sourceAndTarget.split(' -> ')[0]
	target = sourceAndTarget.split(' -> ')[1]

	source = source.strip()
	target = target.strip()

	localType = globalType

	if( i != len(relationships) - 1):
		if( degree0Node.strip().lower() == source.strip().lower() ):
			localType = 'licensing'

		stringToWrite = '\t{source: "' + source + '", target: "' + target + '", type: "' + localType + '"},\n'
	else:
		if( degree0Node.strip().lower() == source.strip().lower() ):
			localType = 'licensing'

		stringToWrite = '\t{source: "' + source + '", target: "' + target + '", type: "' + localType + '"}\n'

	outputFile.write(stringToWrite)
	i = i + 1
...