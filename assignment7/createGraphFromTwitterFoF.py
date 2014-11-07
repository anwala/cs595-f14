from bs4 import BeautifulSoup
import os, sys

degree0Node = 'Dr. Nelson'
globalType = 'suit'
try:
	inputFile = open('multiDegreeFriends.txt', 'r')
	outputFile = open('twitterWhosFollowingWho.txt', 'w')

	relationships = inputFile.readlines()
	inputFile.close()
except:
	exc_type, exc_obj, exc_tb = sys.exc_info()
	fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
	print fname, exc_tb.tb_lineno, sys.exc_info()



outputFile.write('var links = \n[\n')

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

outputFile.write('];\n')

outputFile.close()