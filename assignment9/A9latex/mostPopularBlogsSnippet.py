...
#Limit the number of terms to the most "popular" (i.e., frequent) 500 terms
#sort by frequency
arrayOfTermTermFrequencyTuples = sorted(arrayOfTermTermFrequencyTuples, key=lambda tup: tup[1], reverse=True)
if( len(arrayOfTermTermFrequencyTuples) > 0 ):
	
	for termFrequencyTuple in  arrayOfTermTermFrequencyTuples:
		term = termFrequencyTuple[0]
		termFrequency = termFrequencyTuple[1]

		#print term, termFrequency

		#get 500 most popular terms
		if( len(wordlist) <= 500 ):
			wordlist.append(term)
		else:
			break
...