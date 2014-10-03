import commands
import os, sys
import hashlib
#from bs4 import BeautifulSoup
from os import walk
import math

import re
#first line is label, subsequent lines have format <uri, ...>
inputFileName = 'URIs.txt'
#<uri, md5hash>
uriHashDictionary = {}

totalNumberOfDocumentInCorpus = 20000000000
documentWithTerm = 206000000

def getInput():

	try:
		urlsFile = open(inputFileName)
		listOfURIs = urlsFile.readlines()

		if(len(listOfURIs) > 0):
			del listOfURIs[0]
			for u in listOfURIs:

				u = u.split(', ')
				u = u[0] 
				md5hashFilename = getHashFromURI(u)
				uriHashDictionary[u] = md5hashFilename

	except:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		print(fname, exc_tb.tb_lineno, sys.exc_info() )
		return


	return listOfURIs

def getHashFromURI(uri):

	md5hash = ''

	if( len(uri) > 0 ):
		# Assumes the default UTF-8; http://www.pythoncentral.io/hashing-strings-with-python/
		hash_object = hashlib.md5(uri.encode())
		md5hash = hash_object.hexdigest()

	return md5hash

def extractHTMLAndSave():

	if( len(uriHashDictionary) > 0 ):
		count = 0
		for uri in uriHashDictionary:

			filename =  str(count) + '-' + uriHashDictionary[uri] + '.html'
			co = 'curl -s -L ' + uri + ' > ./RawHtml/' + filename
			
			commands.getoutput(co)
			count = count + 1

def processHTMLAndSave():

	if( len(uriHashDictionary) > 0 ):

		count = 0

		for uri in uriHashDictionary:
			
			filename = str(count) + '-' + uriHashDictionary[uri] + '.html'
			count = count + 1

			try:
				co = 'lynx -dump -force_html ' + uri
				processedFileText = commands.getoutput(co)

				outputHtmlFile = open('./ProcessedHtml/processed_' + filename, 'w')
				outputHtmlFile.write(processedFileText)
				outputHtmlFile.close()

			except:
				exc_type, exc_obj, exc_tb = sys.exc_info()
				fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
				print(fname, exc_tb.tb_lineno, sys.exc_info() )
				return

def processHTMLAndSave_old(listOfURIs):

	if( len(listOfURIs) > 0 ):

		filenames = next(os.walk('./RawHtml/'))[2]

		for filename in filenames:		
			
			try:
				
				htmlFile = open('./RawHtml/'+filename, 'r')
				htmlFileText = htmlFile.read()
				htmlFile.close()

				
				processedFileText = ''.join( BeautifulSoup( htmlFileText ).findAll( text = True ) ) 


				outputHtmlFile = open('./ProcessedHtml/processed_' + filename, 'w')
				outputHtmlFile.write(processedFileText)
				outputHtmlFile.close()

			except:
				#htmlFile.close()
				exc_type, exc_obj, exc_tb = sys.exc_info()
				fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
				#print(fname, exc_tb.tb_lineno, sys.exc_info() )
				#return

def getWordCountFromInFile(filename):

	wordCount = 0
	if( len(filename) > 0 ):
		try:
			co = 'wc -w ' + filename
			wordCount = commands.getoutput(co)
			wordCount = wordCount.split(' ')[0]
		except:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(fname, exc_tb.tb_lineno, sys.exc_info() )

	return wordCount

def countTheNumberOfOccurencesInFile(filename, word):

	count = 0
	if( len(filename) > 0 ):

		try:
			inputFileName = open(filename, 'r')
			inputString = inputFileName.read()

			inputFileName.close()
			word = word.lower()
			inputString = inputString.lower()

			#count = len(re.findall("\\b"+word+"\\b", inputString)) for exactness
			count = inputString.count(word)#for substring
		except:
			inputFileName.close()
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(fname, exc_tb.tb_lineno, sys.exc_info() )


	

	return count

def logBase2(number):
	return math.log(number) / math.log(2)

def calculateTFIDFforUris(filenamesOfHits, term):

	uri_TFIDF_TF_IDF_tuples = []
	if( len(filenamesOfHits) > 0 ):


		#TF-IDF = TF * IDF = occurrence in doc / words in doc * log2(total docs in corpus / docs with term)
		
		for f in filenamesOfHits:

			f = './ProcessedHtml/'+f
			occurrenceInDoc = countTheNumberOfOccurencesInFile(f, term)
			wordsInDoc = getWordCountFromInFile(f)

			hashFilename = f.split('-')
			hashFilename = hashFilename[1].split('.')[0]
			uri = [key for key, value in uriHashDictionary.iteritems() if value == hashFilename][0]

			TF = ( float(occurrenceInDoc) / float(wordsInDoc) )
			IDF = logBase2( float(totalNumberOfDocumentInCorpus) / float(documentWithTerm) )
			TFIDF = TF * IDF

			#print uri, ": ", occurrenceInDoc, wordsInDoc, TFIDF

			uriTuple = (uri, TFIDF, TF, IDF)
			uri_TFIDF_TF_IDF_tuples.append(uriTuple)

	return uri_TFIDF_TF_IDF_tuples

#urisTuple: <uri, TDIDF, TF, IDF>
def printTableFromTuple(urisTuple, numberOfItemsToPrint=10):

	if( len(urisTuple) > 0 and numberOfItemsToPrint < len(urisTuple) ):
		urisTuple = sorted(urisTuple, key=lambda uriEntry: uriEntry[2])

		for i in range(0, 10):

			URI = urisTuple[i][0]
			TFIDF = urisTuple[i][1]
			TF = urisTuple[i][2]
			IDF = urisTuple[i][3]
			
			print TFIDF, TF, IDF, URI


def seekForStringInFiles(stringInput):

	filenamesOfHits = []
	if( len(stringInput)  > 0):

		filenames = next(os.walk('./ProcessedHtml/'))[2]

		count = 0
		for filename in filenames:		
			
			try:
				
				co = 'cat ' + './ProcessedHtml/' + filename + ' | grep ' + stringInput
				output = commands.getoutput(co)

				if( len(output) > 0 ):
					count = count + 1
					filenamesOfHits.append(filename)
					#print output
					#print ""

			except:

				exc_type, exc_obj, exc_tb = sys.exc_info()
				fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
				print(fname, exc_tb.tb_lineno, sys.exc_info() )


	return filenamesOfHits



#populate dictionary with <uri, hash> tuple
getInput()#0

#to do
#extractHTMLAndSave()#1

#processHTMLAndSave()#2

message = 'plan'#3
filenamesOfHits = seekForStringInFiles(message)#3
print "Hits count: ", len(filenamesOfHits)
urisTuple = calculateTFIDFforUris(filenamesOfHits, message)#3
printTableFromTuple(urisTuple)#3




#picture = 1
#message = 2
#plan = 4
