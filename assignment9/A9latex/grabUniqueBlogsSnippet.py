#grab 100 unique blogs
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
getNUniqueBlogs(100)