#cluster and plot dendogram
def plotHierarchicalClustering(items2dArray, maxClusterCount, labelArray, searchItemCount):
	if( len(items2dArray) > 0 and len(items2dArray) >= maxClusterCount and searchItemCount > 0):

		distances = hierarchicalClustering.distance.pdist(items2dArray)

		linkages = hierarchicalClustering.linkage(distances, method='complete')
		clusterData = hierarchicalClustering.fcluster(linkages, maxClusterCount, 'maxclust')

		clusterClusterItemsDict = {}

		# calculate labels and count the number of items in each cluster
		#labels=list('' for i in range(len(items2dArray)))
		for i in range(len(items2dArray)):
			
			#labels[i]=str(i)+ ',' + str(clusterData[i])
			#print clusterData[i]
			clusterIndex = clusterData[i]
			clusterClusterItemsDict.setdefault(clusterIndex, [])
			clusterClusterItemsDict[clusterIndex].append(i)

		# calculate color threshold
		ct=linkages[-(maxClusterCount-1),2]  

		#print clusterClusterCountDict
		showPlotFlag = False
		for clusterIndex, clusterItemsArray in clusterClusterItemsDict.items():
			if( searchItemCount == len(clusterItemsArray) ):
				print 'yes, maxClusterCount: ', maxClusterCount
				print clusterClusterItemsDict[clusterIndex]
				showPlotFlag = True
				break

		if( showPlotFlag ):
			#plot
			P =hierarchicalClustering.dendrogram(linkages, labels = labelArray, color_threshold = ct)
			plt.show()