import feedparser
import re
import os, sys

'''
  input: feed.xml, fisherclassifier, trainingAndTestDataFileName.txt, ['train'|'test'], stopAtVCount, 'getWord'|'getEntry'
'''
def nonInteractiveRead(feed, classifier, trainingAndTestDataFileName, mode, maxItems, getWordGetEntryMethod='getWord'):

  if( len(feed) > 0 and len(trainingAndTestDataFileName) > 0 and (mode == 'train' or mode == 'test') and maxItems > 0 and (getWordGetEntryMethod == 'getWord' or getWordGetEntryMethod == 'getEntry')):

    #trainingAndTestDataFileName: <title, titleText, classLabel>
    try:
      inputFile = open(trainingAndTestDataFileName, 'r')

      if( mode == 'test' ):
        prefix = trainingAndTestDataFileName.split('.')[0]
        outputFile = open(prefix+'Predictions.txt', 'w')

      lines = inputFile.readlines()
      inputFile.close()
      #first line is schema
      del lines[0]
      print len(lines), 'lines read from ' + trainingAndTestDataFileName
    except:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(fname, exc_tb.tb_lineno, sys.exc_info() )
      return

    if( mode == 'test' ):
      outputFile.write('TITLE, CPROB, PREDICTED-LABEL, ACTUAL-LABEL\n')

    # Get feed entries and loop over them
    f=feedparser.parse(feed)
    count = 1
    for entry in f['entries']:

      for l in lines:

        titleContentLabel = l.split(' <> ')

        title = titleContentLabel[0].strip()
        summary = titleContentLabel[1].strip()
        actualClassLabel = titleContentLabel[2].strip()

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

            print '...testing model', count

            stringToWrite = title + ', ' + str(cProbValue) + ', ' + prediction + ', ' + actualClassLabel
            print stringToWrite
            outputFile.write(stringToWrite + '\n')

          if(count == maxItems):
            print '...max items reached, closing'

            if( mode == 'test' ):
              outputFile.close()

            return

          count += 1

    if( mode == 'test' ):
      outputFile.close()

    
# Takes a filename of URL of a blog feed and classifies the entries
def read(feed,classifier):

  print feed

  # Get feed entries and loop over them
  f=feedparser.parse(feed)
  for entry in f['entries']:
    print
    print '-----'
    # Print the contents of the entry
    print 'Title:     '+entry['title'].encode('utf-8')
    #mod1 preve:#print 'Publisher: '+entry['publisher'].encode('utf-8')
    #print 'Publisher: '+entry['publisher'].encode('utf-8')
    print
    #print entry['summary'].encode('utf-8')
    

    # Combine all the text to create one item for the classifier
    #mod2 prev:#fulltext='%s\n%s\n%s' % (entry['title'],entry['publisher'],entry['summary'])
    fulltext='%s\n%s' % (entry['title'],entry['summary'])

    # Print the best guess at the current category
    #print 'Guess: '+str(classifier.classify(entry))
    print 'Guess: '+str(classifier.classify(fulltext))
    print 'globalCProbValue:', classifier.getGlobalCProbValue()


    # Ask the user to specify the correct category and train on that
    #mod3 prev:?
    cl=raw_input('Enter category: ')
    classifier.train(fulltext,cl)
    #classifier.train(entry,cl)
    # where fulltext is now title + summary




def entryfeatures(entry):
  print '.....................getF'
  splitter=re.compile('\\W*')
  f={}
  
  #debug - start
  #splitter.split(entry['title'])
  #debug - end

  # Extract the title words and annotate
  titlewords=[s.lower() for s in splitter.split(entry['title']) 
          if len(s)>2 and len(s)<20]
  for w in titlewords: f['Title:'+w]=1
  
  # Extract the summary words
  summarywords=[s.lower() for s in splitter.split(entry['summary']) 
          if len(s)>2 and len(s)<20]

  # Count uppercase words
  uc=0
  for i in range(len(summarywords)):
    w=summarywords[i]
    f[w]=1
    if w.isupper(): uc+=1
    
    # Get word pairs in summary as features
    if i<len(summarywords)-1:
      twowords=' '.join(summarywords[i:i+1])
      f[twowords]=1
    
  # Keep creator and publisher whole
  #f['Publisher:'+entry['publisher']]=1

  # UPPERCASE is a virtual word flagging too much shouting  
  if float(uc)/len(summarywords)>0.3: f['UPPERCASE']=1
  
  return f
