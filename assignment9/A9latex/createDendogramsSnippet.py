#create dendograms
def createAsciiDendogram():
	blognames,words,data=clusters.readfile('blogVector.txt')
	clust=clusters.hcluster(data)

	clusters.printclust(clust,labels=blognames)

def creatJPegDendogram():
	blognames,words,data=clusters.readfile('blogVector.txt')
	clust=clusters.hcluster(data)
	clusters.drawdendrogram(clust,blognames,jpeg='blogclust.jpg')