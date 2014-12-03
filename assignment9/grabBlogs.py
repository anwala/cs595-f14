import requests
import urlparse
from bs4 import BeautifulSoup
import os, sys

import feedparser
import re
import clusters
import math

def followTheRedirectCurl(url):
	if(len(url) > 0):

		try:
			r = requests.head(url, allow_redirects=True)
			return r.url
		except:
			return ''
	else:

		return ''

'''
	input: http://blogName.blogspot.com/
'''
def listOfPageFeeds(blogUrl):

	listOfPageFeeds = []
	if( len(blogUrl) > 0 ):

		if( blogUrl[-1:] != '/' ):
			blogUrl = blogUrl + '/feeds/posts/default?max-results=500'
			#blogUrl = blogUrl + '/feeds/posts/default/'
		else:
			blogUrl = blogUrl + 'feeds/posts/default?max-results=500'
			#blogUrl = blogUrl + 'feeds/posts/default/'

		listOfPageFeeds = []
		#listOfPageFeeds.append(blogUrl)
		listOfPageFeeds = recursivelyGetFeedPagesForBlog(blogUrl, listOfPageFeeds)

	
	return listOfPageFeeds

'''
	input: http://blogName.blogspot.com/
'''
def listOfPageFeedsPageCount(blogUrl):

	listOfPageFeeds = []
	if( len(blogUrl) > 0 ):

		if( blogUrl[-1:] != '/' ):
			blogUrl = blogUrl + '/feeds/posts/default/'
		else:
			blogUrl = blogUrl + 'feeds/posts/default/'

		listOfPageFeeds = []
		#listOfPageFeeds.append(blogUrl)
		listOfPageFeeds = recursivelyGetFeedPagesForBlog(blogUrl, listOfPageFeeds)

	
	return listOfPageFeeds

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

		#entriesInBlog = soup.findAll('entry')
		#print len(entriesInBlog)

	return listOfPages

def getUniqueBlogs(countOfBlogsToRetrieve):

	listOfBlogs = []
	if( countOfBlogsToRetrieve>0 ):

		try:
			outputFile = open('blogs.txt', 'w')
			outputFile.write('http://f-measure.blogspot.com/\n')
			outputFile.write('http://ws-dl.blogspot.com/\n')
		except:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(fname, exc_tb.tb_lineno, sys.exc_info() )

		while len(listOfBlogs) != countOfBlogsToRetrieve:

			print 'retrieved: ', len(listOfBlogs)
			
			blogUrl = 'http://www.blogger.com/next-blog?navBar=true&blogID=3471633091411211117'
			response = ''
			try:
				response = requests.head(blogUrl, allow_redirects=True)
				response = response.url
			except:
				response = ''


			if len(response) > 0:
				if response not in listOfBlogs:

					response = response.lower()
					
					parsedUrl = urlparse.urlparse(response)
					parsedUrl = parsedUrl.scheme + '://' + parsedUrl.netloc + '/'

					listOfBlogs.append(parsedUrl)
					outputFile.write(parsedUrl + '\n')

		outputFile.close()

def getNUniqueBlogs(count):

	listOfBlogs = []
	if( count>0 ):

		try:
			outputFile = open('listOfUniqueBlogs.txt', 'w')

			outputFile.write('http://f-measure.blogspot.com/\n')
			outputFile.write('http://ws-dl.blogspot.com/\n')
		except:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(fname, exc_tb.tb_lineno, sys.exc_info() )

		while len(listOfBlogs) != count:
			
			blogUrl = 'http://www.blogger.com/next-blog?navBar=true&blogID=3471633091411211117'
			finalBlog = followTheRedirectCurl(blogUrl)

			if len(finalBlog) > 0:
				if finalBlog not in listOfBlogs:

					finalBlog = finalBlog.lower()
					
					parsedUrl = urlparse.urlparse(finalBlog)
					parsedUrl = parsedUrl.scheme + '://' + parsedUrl.netloc + '/'

					listOfBlogs.append(parsedUrl)
					outputFile.write(parsedUrl + '\n')

		outputFile.close()

def consolidateDictionaries(dictA, dictB):

	if( len(dictA) > 0 and len(dictB) > 0 ):
		for term, termFrequency in dictB.items():

			if( term in dictA ):
				dictA[term] = dictA[term] + termFrequency# or dictA[term] = dictA[term] + dictB[term]
			else:
				dictA[term] = termFrequency# or dictA[term] = dictB[term]

		return dictA
	else:

		return {}

def logBase2(number):
	return math.log(number) / float(math.log(2))

#From Programming Collective Intelligence, Toby Segaran - start
def getwords(html):
    # Remove all the HTML tags
    txt = re.compile(r'<[^>]+>').sub('', html)

    # Split words by all non-alpha characters
    words = re.compile(r'[^A-Z^a-z]+').split(txt)

    # Convert to lowercase
    return [word.lower() for word in words if word != '']

def getwordcounts(url):
	
	'''
	Returns title and dictionary of word counts for an RSS feed
	'''
	# Parse the feed


	#url: http://blogName.blogspot.com/
	d = feedparser.parse(url)


	wc = {}

	# Loop over all the entries
	for e in d.entries:
		if 'summary' in e:
			summary = e.summary
		else:
			summary = e.description

		# Extract a list of words
		words = getwords(e.title + ' ' + summary)
		for word in words:
			wc.setdefault(word, 0)
			wc[word] += 1

	return (d.feed.title, wc)

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


			print 'l: ', len(dictionaryOfPageCounts)
			if( len(dictionaryOfPageCounts) == maxCountOfBlogsToExplore ):
				break


		outputFile.write('PageCount PageCountFrequency \n')
		if( len(dictionaryOfPageCounts) > 0 ):
			for pageCount, pageCountFrequency in dictionaryOfPageCounts.items():
				outputFile.write(str(pageCount) + ' ' + str(pageCountFrequency) + '\n')

		outputFile.close()

#modified to look at all pages of the blog
def generateFeedVector(countOfBlogsToExplore=10):

	if( countOfBlogsToExplore > 0 ):


		apcount = {}
		wordcounts = {}
		feedlist = [line for line in file('100listOfUniqueBlogs.txt')]

		iteration = 1
		
		for feedurl in feedlist:

			print 'blogCount: ', iteration
			
			feedurl = feedurl.strip()

			try:
				#(title, wc) = getwordcounts(feedurl + 'feeds/posts/default/')
				(title, wc) = getwordcounts(feedurl + 'feeds/posts/default?max-results=500')

				#get wc for other pages - start
				
				listOfFeedPages = listOfPageFeeds(feedurl)

				#print '...bef', title, len(wc)
				for feedPage in listOfFeedPages:
					feedPage = feedPage.strip()
					(sameTitle, nextPageWordCount) = getwordcounts(feedPage)

					consolidateDictionaries(wc, nextPageWordCount)
				
				#print '...aft', title, len(wc)
				
				#get wc for other pages - encoded

				#this wc is consolidated
				wordcounts[title] = wc
				for (word, count) in wc.items():
					apcount.setdefault(word, 0)
					if count > 1:
						apcount[word] += 1

				
				#print '...tot', len(apcount)

			except:
				print 'Failed to parse feed %s' % feedurl
				exc_type, exc_obj, exc_tb = sys.exc_info()
				fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
				print(fname, exc_tb.tb_lineno, sys.exc_info() )


			if( countOfBlogsToExplore == iteration ):
				break

			iteration += 1


		wordlist = []

		#print apcount
		
		arrayOfTermTermFrequencyTuples = []
		for (term, termFrequency) in apcount.items():

			#print 'w:', term, 'bc:', termFrequency
			frac = float(termFrequency) / len(feedlist)

			#print '...frac', frac
			if frac > 0.1 and frac < 0.5:
				#wordlist.append(term)
				
				termTermFrequencyTuple = (term, termFrequency)
				arrayOfTermTermFrequencyTuples.append(termTermFrequencyTuple)
				#print '......frac', frac


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
		

		out = file('blogVector.txt', 'w')
		out.write('Blog')

		for word in wordlist:
			word = word.encode('ascii', 'ignore')
			out.write('\t%s' % word)

		out.write('\n')
		for (blog, wc) in wordcounts.items():
			
			blog = blog.encode('ascii', 'ignore')
			#print blog
			out.write(blog)
			for word in wordlist:

				word = word.encode('ascii', 'ignore')
				if word in wc:
					out.write('\t%d' % wc[word])
				else:
					out.write('\t0')
			out.write('\n')

def getFeedVector(blogsFilename):

	apcount = {}
	wordcounts = {}
	feedlist = [line for line in file(blogsFilename)]

	
	
	for feedurl in feedlist:
		
		feedurl = feedurl.strip()

		try:
			
			(title, wc) = getwordcounts(feedurl + 'feeds/posts/default?max-results=500')
			wordcounts[title] = wc
			for (word, count) in wc.items():
				apcount.setdefault(word, 0)
				if count > 1:
					apcount[word] += 1

		except:
			print 'Failed to parse feed %s' % feedurl
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(fname, exc_tb.tb_lineno, sys.exc_info() )



	wordlist = []
	listOfTermTermFrequencyTuple = []
	for (t, tF) in apcount.items():

		frac = float(tF) / len(feedlist)

		if frac > 0.1 and frac < 0.5:
			ttFTuple = (t, tF)
			listOfTermTermFrequencyTuple.append(ttFTuple)


	#frequent 500 terms
	listOfTermTermFrequencyTuple = sorted(listOfTermTermFrequencyTuple, key=lambda tuple: tuple[1], reverse=True)
	for ttF in  listOfTermTermFrequencyTuple:
		t = ttF[0]
		tF = ttF[1]

		if( len(wordlist) > 500 ):
			break
		else:
			wordlist.append(t)
	

	out = file('blogVectorResult.txt', 'w')
	out.write('Blog')

	for word in wordlist:
		word = word.encode('ascii', 'ignore')
		out.write('\t%s' % word)

	out.write('\n')
	for (blog, wc) in wordcounts.items():
		
		blog = blog.encode('ascii', 'ignore')
		#print blog
		out.write(blog)
		for word in wordlist:

			word = word.encode('ascii', 'ignore')
			if word in wc:
				out.write('\t%d' % wc[word])
			else:
				out.write('\t0')
		out.write('\n')

def generateFeedVectorTFIDFVersion(countOfBlogsToExplore=10):

	if( countOfBlogsToExplore > 0 ):


		apcount = {}
		wordcounts = {}
		feedlist = [line for line in file('100listOfUniqueBlogs.txt')]

		iteration = 1
		
		for feedurl in feedlist:

			print 'blogCount: ', iteration
			
			feedurl = feedurl.strip()

			try:
				(title, wc) = getwordcounts(feedurl + 'feeds/posts/default/')

				#get wc for other pages - start
				
				listOfFeedPages = listOfPageFeeds(feedurl)

				#print '...bef', title, len(wc)
				for feedPage in listOfFeedPages:
					feedPage = feedPage.strip()
					(sameTitle, nextPageWordCount) = getwordcounts(feedPage)

					consolidateDictionaries(wc, nextPageWordCount)
				
				#print '...aft', title, len(wc)
				
				#get wc for other pages - encoded

				#this wc is consolidated
				wordcounts[title] = wc
				for (word, count) in wc.items():
					apcount.setdefault(word, 0)
					if count > 1:
						apcount[word] += 1

				#print '...tot', len(apcount)

			except:
				print 'Failed to parse feed %s' % feedurl
				exc_type, exc_obj, exc_tb = sys.exc_info()
				fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
				print(fname, exc_tb.tb_lineno, sys.exc_info() )


			if( countOfBlogsToExplore == iteration ):
				break

			iteration += 1


		wordlist = []

		#print apcount
		
		arrayOfTermTermFrequencyTuples = []
		for (term, termFrequency) in apcount.items():

			#print 'w:', term, 'bc:', termFrequency
			frac = float(termFrequency) / len(feedlist)

			#print '...frac', frac
			if frac > 0.1 and frac < 0.5:
				#wordlist.append(term)
				
				termTermFrequencyTuple = (term, termFrequency)
				arrayOfTermTermFrequencyTuples.append(termTermFrequencyTuple)
				#print '......frac', frac


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
		

		out = file('blogVectorTFIDFVersion.txt', 'w')
		out.write('Blog')

		for word in wordlist:
			word = word.encode('ascii', 'ignore')
			out.write('\t%s' % word)

		out.write('\n')
		for (blog, wc) in wordcounts.items():
			
			blog = blog.encode('ascii', 'ignore')
			#print blog
			out.write(blog)
			for word in wordlist:

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
			out.write('\n')

def createAsciiDendogram():
	blognames,words,data=clusters.readfile('blogVector.txt')
	clust=clusters.hcluster(data)

	clusters.printclust(clust,labels=blognames)

def createJPegDendogram():

	'''
	blognames,words,data=clusters.readfile('blogVector.txt')
	clust=clusters.hcluster(data)
	clusters.drawdendrogram(clust,blognames,jpeg='blogclust.jpg')
	'''
	


	
	blognames,words,data=clusters.readfile('blogVectorTFIDFVersion.txt')
	clust=clusters.hcluster(data)
	clusters.drawdendrogram(clust,blognames,jpeg='blogclustTFIDFVersion.jpg')
	

def createKMeansClusters(kValue):

	if( kValue>0 ):
		blognames,words,data=clusters.readfile('blogVector.txt')
		kclust=clusters.kcluster(data,k=kValue)

		count = 0
		for cluster in kclust:

			if( len(cluster) > 0 ):
				print 'cluster', count
				for instance in cluster:
					print '...',blognames[instance]

				count += 1

def createMDS():
	blognames,words,data=clusters.readfile('blogVector.txt')
	coords,iterationCount=clusters.scaledown(data)
	clusters.draw2d(coords,blognames,jpeg='blogs2d.jpg')

	print 'iterationCount', iterationCount


#From Programming Collective Intelligence, Toby Segaran - end

#problem 1
#getNUniqueBlogs(130)


# get
'''
feedPages = listOfPageFeeds('http://sushicat11.blogspot.com/')
print len(feedPages)
'''


'''
returnDict = getwordcounts('http://f-measure.blogspot.com/feeds/posts/default')
print returnDict
'''

#generateFeedVector(100)
#getBlogPageCount(100)

#problem 2
#createAsciiDendogram()
#createJPegDendogram()

#problem 3
#createKMeansClusters(5)
#createKMeansClusters(10)
#createKMeansClusters(20)

#problem 4
#createMDS()

#problem5
#generateFeedVectorTFIDFVersion(100)
#createJPegDendogram()
#comment out second block

getFeedVector('inputBlogFile.txt')