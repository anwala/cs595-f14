#MDS 
def createMDS():
	blognames,words,data=clusters.readfile('blogVector.txt')
	coords,iterationCount=clusters.scaledown(data)
	clusters.draw2d(coords,blognames,jpeg='blogs2d.jpg')

	print 'iterationCount', iterationCount