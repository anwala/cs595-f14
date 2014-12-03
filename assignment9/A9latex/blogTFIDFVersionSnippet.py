generateFeedVector()
...
	word = word.encode('ascii', 'ignore')
	if word in wc:

		#tf for this word:
		termFrequency = wc[word]/float(len(wc))
		#idf
		inverseDocumentFrequency = logBase2(iteration/float(apcount[word]))
		#tfidf
		tfIdf = termFrequency*inverseDocumentFrequency

		#print '...tfIdf', tfIdf

		out.write('\t%f' % tfIdf)
	else:
		out.write('\t0')
...