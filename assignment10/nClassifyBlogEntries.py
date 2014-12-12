import docclass
import feedfilter
import os, sys
import commands

'''
	input: trainingInputFileName.txt, entriesXMLFileName.xml, ['test'|'train'], stopAtCount, 'getWord'|'getEntry'
'''
def myFisherModelInTrainingAndTesting(trainingInputFileName, entriesXMLFileName, dbFileName, mode, maxItems, getWordGetEntryMethod='getWord'):

	if( (mode == 'train' or mode == 'test') and (getWordGetEntryMethod == 'getWord' or getWordGetEntryMethod == 'getEntry') ):

		if( len(trainingInputFileName) > 0 and len(entriesXMLFileName) > 0 and len(dbFileName) > 0 and maxItems > 0 ):

			if( getWordGetEntryMethod == 'getWord' ):
				cl=docclass.fisherclassifier(docclass.getwords)
			else:
				cl=docclass.fisherclassifier(feedfilter.entryfeatures)

			
			cl.setdb(dbFileName)
			feedfilter.nonInteractiveRead(entriesXMLFileName, cl, trainingInputFileName, mode, maxItems, getWordGetEntryMethod)

def getClassLabel(inputTrainingDataFileName):

	if( len(inputTrainingDataFileName) > 0 ):
		#print <classLabel, classLabelCount>
		try:
			inputFile = open(inputTrainingDataFileName, 'r')
			lines = inputFile.readlines()
			#first line is scheman
			#del lines[0]
			print len(lines), 'lines read from blogTrainingData.txt'
			inputFile.close()
		except:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(fname, exc_tb.tb_lineno, sys.exc_info() )
			return


		itemItemCountDictionary = {}
		for l in lines:
			item = l.split(' <> ')
			item = item[2].strip()

			itemItemCountDictionary.setdefault(item, 0)
			itemItemCountDictionary[item] += 1

		print itemItemCountDictionary

'''
	input:
		blogUrl:
			'http://blogNameHere.blogspot.com/'
		outputXMLFileName:
			'blogEntries.xml'
'''
def getXMLEntriesFromBlog(blogUrl, outputXMLFileName, maximumEntries=10):

	if( len(blogUrl) > 0 and len(outputXMLFileName) > 0 and maximumEntries > 0 ):
		maximumEntries = str(maximumEntries)
		blogUrl = blogUrl.strip()

		try:
			
			#dictionaryOfEntryTitleEntryContent = getDictionaryOfBlogData(blogUrl + 'feeds/posts/default?max-results='+maximumEntries)

			co = 'curl -s ' + blogUrl + 'feeds/posts/default?max-results='+maximumEntries
			output = commands.getoutput(co)

			outputFile = open(outputXMLFileName, 'w')
			outputFile.write(output)
			outputFile.close()

		except:
			print 'Failed to parse feed %s' % blogUrl
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(fname, exc_tb.tb_lineno, sys.exc_info() )

def formattingFunction():


	#print <classLabel, classLabelCount>
	try:
		inputFile = open('50nBlogTrainingDataSource.txt', 'r')
		lines = inputFile.readlines()
		#first line is scheman
		del lines[0]
		print len(lines), 'lines read from blogTrainingData.txt'
	except:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		print(fname, exc_tb.tb_lineno, sys.exc_info() )
		return


	#itemItemCountDictionary = {}
	count = 1
	for l in lines:
		item = l.split(' <> ')
		print str(count) + '	&	' + item[0].strip() + '	&	'+ item[2].strip() + '<*>'

		count += 1
		'''
		item = item[2].strip()

		itemItemCountDictionary.setdefault(item, 0)
		itemItemCountDictionary[item] += 1
		'''

	#print itemItemCountDictionary

#formattingFunction()
#get blobs
#p1
numberOfBlogEntriesToProcess = 300
blogName = 'stevegilliard'
blogUrl = 'http://' + blogName + '.blogspot.com/'
outputXMLFileName = blogName + '.xml'
#getXMLEntriesFromBlog(blogUrl, outputXMLFileName, numberOfBlogEntriesToProcess)


#print class labels
'''
inputTrainingDataFileName = 'nBlogTrainingDataSource.txt'
getClassLabel(inputTrainingDataFileName)
inputTrainingDataFileName = '50nBlogTrainingDataSource.txt'
getClassLabel(inputTrainingDataFileName)
inputTrainingDataFileName = '50nBlogTestDataSource.txt'
getClassLabel(inputTrainingDataFileName)
'''

#p2
numberOfEntriesToTrainTest = 50
dbFileName = blogName +'.db'
#train
#inputTrainingDataFileName = '50nBlogTrainingDataSource.txt'
#myFisherModelInTrainingAndTesting(inputTrainingDataFileName, outputXMLFileName, dbFileName, 'train', numberOfEntriesToTrainTest)

#test
inputTrainingDataFileName = '50nBlogTestDataSource.txt'
#myFisherModelInTrainingAndTesting(inputTrainingDataFileName, outputXMLFileName, dbFileName, 'test', numberOfEntriesToTrainTest)

#p3: run calculatePrecision.py

#p4
#part 1
#numberOfEntriesToTrainTest = 90
#dbFileName = '90nBlogTrainingDataSource.db'
#train
#inputTrainingDataFileName = '90nBlogTrainingDataSource.txt'
#myFisherModelInTrainingAndTesting(inputTrainingDataFileName, outputXMLFileName, dbFileName, 'train', numberOfEntriesToTrainTest)

#test
#numberOfEntriesToTrainTest = 10
#inputTrainingDataFileName = '10nBlogTestDataSource.txt'
#myFisherModelInTrainingAndTesting(inputTrainingDataFileName, outputXMLFileName, dbFileName, 'test', numberOfEntriesToTrainTest)

#table of precision/recall/f1 for 10, confusion matrix - have this
#run calculatePrecision.py with 10nBlogTestDataSourcePredictions.txt
#part 2
#train
numberOfEntriesToTrainTest = 50
dbFileName = '50nBlogTrainingDataSourcePart4.db'
#train
#inputTrainingDataFileName = '50nBlogTrainingDataSource.txt'
#myFisherModelInTrainingAndTesting(inputTrainingDataFileName, outputXMLFileName, dbFileName, 'train', numberOfEntriesToTrainTest, 'getEntry')


#test
inputTrainingDataFileName = '50nBlogTestDataSource.txt'
myFisherModelInTrainingAndTesting(inputTrainingDataFileName, outputXMLFileName, dbFileName, 'test', numberOfEntriesToTrainTest, 'getEntry')

#table of cprob/actual/prediction
#50/50: table of precision/recall/f1 - #run calculatePrecision.py for 50nBlogTestDataSourcePredictions.txt
#which is better 50/50 getWord or 50/50 getEntry, why
