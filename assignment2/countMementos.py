import commands
import os, sys

globalMementoUrlDateTimeDelimeter = "*+*+*"
def getMementosPages(url):

	if(len(url)>0):

		pages = []
		timemapCount = 0
		timemapPrefix = 'http://mementoproxy.cs.odu.edu/aggr/timemap/link/1/' + url
		while( True ):

			co = 'curl --silent ' + timemapPrefix
			page = commands.getoutput(co)	
			pages.append(page)

			indexOfRelTimemapMarker = page.rfind('>;rel="timemap"')

			if( indexOfRelTimemapMarker == -1 ):
				break
			else:
				#retrieve next timemap for next page of mementos e.g retrieve url from <http://mementoproxy.cs.odu.edu/aggr/timemap/link/10001/http://www.cnn.com>;rel="timemap"
				i = indexOfRelTimemapMarker -1
				timemapPrefix = ''
				while( i > -1 ):
					if(page[i] != '<'):
						timemapPrefix = page[i] + timemapPrefix
					else:
						break
					i = i - 1

			
			
		return pages
	else:
		print "url length = 0"

def getItemGivenSignature(page):

	if( len(page) > 0 ):
		splitPages0 = page.split(', <')

		listOfItems = []


		for i in range(1, len(splitPages0)):

			#splitPagesAgain[url,rel,datetime]
			if( splitPages0[i].find(';') > -1 ):
				splitPagesAgain = splitPages0[i].split(';')

				#memento signature
				if( splitPagesAgain[1] == 'rel="memento"' ):

					url = splitPagesAgain[0]
					url = url[0:len(url)-1]

					
					if(len(splitPagesAgain)>2):
						if( splitPagesAgain[2].find(' datetime="')> -1 ):
							date = splitPagesAgain[2].strip(' datetime="')
							date = date[0:len(date)-2]

					#print url , globalMementoUrlDateTimeDelimeter, date
					listOfItems.append(url + globalMementoUrlDateTimeDelimeter + date)
		
		return listOfItems	

def countMementos(url):

	if(len(url) > 0):
		pages = getMementosPages(url)
		
		countOfMementos = 0
		for i in range(0,len(pages)):
			mementos = getItemGivenSignature(pages[i])

			dummyList = []
			if( type(mementos)== type(dummyList)):
				countOfMementos = countOfMementos + len(mementos)
			

		return countOfMementos
	else:
		return -1

def getMentosCountForFile(inputFilename, outputFilename):
	if(len(inputFilename) > 0 and len(outputFilename) > 0):


		try:
			inputFile = open(inputFilename, 'r')
			inputUrlsList = inputFile.readlines()
			inputFile.close()

			if(len(inputUrlsList) > 0):
				outputFile = open(outputFilename, 'a')

		except:
			inputFile.close()
			outputFile.close()
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(fname, exc_tb.tb_lineno, sys.exc_info() )
			return


		#for i in range(726, 0, -1):
		#for i in range(len(inputUrlsList)-1, 0, -1):
		for i in range(0, len(inputUrlsList)):
		#for i in range(0, 5):
			url = inputUrlsList[i].strip().split(', ')[0]

			mementosCount = countMementos(url)

			stringToWrite = url + ', ' + str(mementosCount) + '\n'
			outputFile.write(stringToWrite)
			print i, stringToWrite

		outputFile.close()



getMentosCountForFile('countMementosInputFile.txt', 'countMementosOutputFile.txt')