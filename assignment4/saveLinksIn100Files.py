inputFileName = '100_parentChildLinks.txt'

#format
'''
parentURI0
	childURI0
	childURI1
parentURI1
	childURI0
	childURI1
.
.
.
parentURI(n-1)
	childURI0
	childURI1
'''
def generateDotFile():
	try:
		inputFile = open(inputFileName)
		
	except:
		inputFile.close()
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		print(fname, exc_tb.tb_lineno, sys.exc_info() )
		return

	lines = inputFile.readlines()
	inputFile.close()

	filename = 'sample.txt'
	if( len(lines) > 0 ):

		count = -1
		for uri in lines:
			
			#is this parent
			uri = uri.lower()
			if( uri[0] == 'h' ):
				count = count + 1
				
				filename = './100Links/' + str(count) + '-' + 'URI.txt'
				
				outputFile = open(filename, 'w')
				outputFile.write(uri)

			else:
				outputFile.write(uri)



generateDotFile()


