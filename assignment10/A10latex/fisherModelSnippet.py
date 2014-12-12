#Fisher model training and testing
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
			
'''
  input: feed.xml, fisherclassifier, trainingAndTestDataFileName.txt, ['train'|'test'], stopAtVCount, 'getWord'|'getEntry'
'''
def nonInteractiveRead(feed, classifier, trainingAndTestDataFileName, mode, maxItems, getWordGetEntryMethod='getWord'):

  if( len(feed) > 0 and len(trainingAndTestDataFileName) > 0 and (mode == 'train' or mode == 'test') and maxItems > 0 and (getWordGetEntryMethod == 'getWord' or getWordGetEntryMethod == 'getEntry')):
...
    if( title.lower() == entry['title'].strip().lower() ):

    #print 'Title:     '+entry['title'].encode('utf-8')
    fulltext='%s\n%s' % (entry['title'],entry['summary'])

    if( mode == 'train' ):
      #training get the correct category and train on that

      if( getWordGetEntryMethod == 'getWord' ):
        classifier.train(fulltext, actualClassLabel)
      else:
       classifier.train(entry, actualClassLabel) 

      print '...training model', count
    else:
      #testing: guess the best guess at the current category
      try:
        if( getWordGetEntryMethod == 'getWord' ):
          prediction = str(classifier.classify(fulltext))
        else:
          prediction = str(classifier.classify(entry))
      except:
        print '...skipping', count
        continue
      
      cProbValue = classifier.getGlobalCProbValue()
...