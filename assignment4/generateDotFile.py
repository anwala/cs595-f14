from urlparse import urlparse
import os, sys
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
inputFileName = '100_parentChildLinks.txt'
outputFileName = 'parentChildURIs.dot'

def compressURLName(url):

	if( len(url) > 0 ):

		url = url.strip()

		u = urlparse(url)

		u = u.netloc
		indexOfName = 0
		if( u.find('www.') > -1 ):
			indexOfName = 1

		uArray = u.split('.')
		
		return uArray[indexOfName]

	else:
		return url

def getCompressedURLName(listOfUncompressedNames):

	compressed = []
	if( len(listOfUncompressedNames) > 0 ):

		for u in listOfUncompressedNames:
			u = u.strip()

			compressedURI = compressURLName(u)
			compressed.append(compressedURI)

	return compressed

def generateDotFile():
	try:
		inputFile = open(inputFileName)
		outputFile = open(outputFileName, 'w')
	except:
		inputFile.close()
		outputFile.close()
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		print(fname, exc_tb.tb_lineno, sys.exc_info() )
		return

	lines = inputFile.readlines()
	inputFile.close()
	currentParent = ''


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


generateDotFile()

'''
digraph unix {
www.uri0.com -> www.cs.odu.edu
www.uri1.com -> www.cs.odu.edu
www.uri0.com [label="Node A"];
www.cs.odu.edu [label="Node A"];
}

digraph ParentChildLinks {
"http://www.rakuten.com/prod/a-study-of-omaha-indian-music/30156865.html?scid=af_linkshare&adid=18094&siteid=mwwap3mifuc-45xozpb3lpijin3bcxyo2w/" -> "https://www.surveymonkey.com/s/fdrhyph"
"http://www.rakuten.com/prod/a-study-of-omaha-indian-music/30156865.html?scid=af_linkshare&adid=18094&siteid=mwwap3mifuc-45xozpb3lpijin3bcxyo2w/" [labels="rakuten"];
"https://www.surveymonkey.com/s/fdrhyph" [labels="surveymonkey"];
}
'''