#Generate blog page count histogram data
def getBlogPageCount(maxCountOfBlogsToExplore=5):

	if( maxCountOfBlogsToExplore > 0 ):

		try:
			inputFile = open('100listOfUniqueBlogs.txt', 'r')
			lines = inputFile.readlines()
			inputFile.close()
			outputFile = open('BLOG-PAGECOUNT.txt', 'w')
		except:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(fname, exc_tb.tb_lineno, sys.exc_info() )


		dictionaryOfPageCounts = {}
		for line in lines:
			line = line.strip()


			listOfFeedPages = listOfPageFeedsPageCount(line)
			pageCount = len(listOfFeedPages) + 1

			dictionaryOfPageCounts.setdefault(pageCount, 0)
			dictionaryOfPageCounts[pageCount] += 1


			if( len(dictionaryOfPageCounts) == maxCountOfBlogsToExplore ):
				break


		outputFile.write('PageCount PageCountFrequency \n')
		if( len(dictionaryOfPageCounts) > 0 ):
			for pageCount, pageCountFrequency in dictionaryOfPageCounts.items():
				outputFile.write(str(pageCount) + ' ' + str(pageCountFrequency) + '\n')

		outputFile.close()

def recursivelyGetFeedPagesForBlog(blogUrl, listOfPages=[]):

	if( len(blogUrl) > 0 ):
		try:
			html = requests.get(blogUrl)
		except:
			countOfPages = 0
		
		soup = BeautifulSoup(html.text)
		nextLink = soup.find('link', { 'rel' : 'next' })

		if nextLink is not None:
			nextLink = nextLink['href']
			listOfPages.append(nextLink)

			recursivelyGetFeedPagesForBlog(nextLink, listOfPages)
	return listOfPages