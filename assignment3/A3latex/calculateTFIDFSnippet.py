#TF-IDF function
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