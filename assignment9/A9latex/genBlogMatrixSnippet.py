#modified to look at all pages of the blog
def generateFeedVector(countOfBlogsToExplore=10):
...
#get wc for other pages - start
	listOfFeedPages = listOfPageFeeds(feedurl)

	#print '...bef', title, len(wc)
	for feedPage in listOfFeedPages:
		feedPage = feedPage.strip()
		(sameTitle, nextPageWordCount) = getwordcounts(feedPage)

		consolidateDictionaries(wc, nextPageWordCount)
	
	#print '...aft', title, len(wc)
	
	#get wc for other pages - encoded
...