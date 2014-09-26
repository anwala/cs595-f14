import os, sys
from urlparse import urlparse


def isStringInList(stringItem, stringList):
	if(len(stringItem) > 0 and len(stringList) > 0):
		for item in stringList:
			if( stringItem == item ):
				return True

	return False

def makeUnique(inputFilename, countOfItemsToWrite):
	if( len(inputFilename) > 0 and countOfItemsToWrite > 0):

		try:
			inputFile = open(inputFilename, 'r')
			inputFileLinesArray = inputFile.readlines()
			inputFile.close()



			if(len(inputFileLinesArray) > 0 and countOfItemsToWrite <= len(inputFileLinesArray) ):
				outputFile = open('uniqueLines_'+inputFilename, 'w')
			else:
				return
		except:
			inputFile.close()
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(fname, exc_tb.tb_lineno, sys.exc_info() )


		outputFileLinesArray = []
		for line in inputFileLinesArray:

			
			#preprocess0
			line = line.strip().split(', ')[0].lower()
			if(line[len(line)-1] != '/'):
				line = line + '/'

			#preprocess1
			#url = urlparse(line)
			#line = 'http://'+ url.netloc + '/'
			#outputFileLinesArray.append(line + '\n')

			
			if(len(outputFileLinesArray) < countOfItemsToWrite):
				line = line.strip().lower()

				#not in list so add
				if( isStringInList(line + '\n', outputFileLinesArray) == False ):
					outputFileLinesArray.append(line + '\n')

			else:
				break
			
			
		try:
			outputFile.writelines(outputFileLinesArray)
			outputFile.close()
		except:
			outputFile.close()
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(fname, exc_tb.tb_lineno, sys.exc_info() )


makeUnique('rawLinks.txt', 1000)



