#create clusters
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