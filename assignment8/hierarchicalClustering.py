import scipy
import scipy.cluster.hierarchy as hierarchicalClustering
import matplotlib.pylab as plt


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

def getInput():
	#inputFile = open('hierarchicalClusterInput1.txt', 'r')
	inputFile = open('hierarchicalClusterInput1.txt', 'r')
	lines = inputFile.readlines()

	items2dArray = []
	labelArray = []
	for l in lines:
		userData = l.strip().split(' ')

		items2dArray.append([float(userData[1]), float(userData[2]), float(userData[3]), float(userData[4]), float(userData[5])])
		labelArray.append(userData[0])
		


	return items2dArray, labelArray



'''
for i in range(1, 30):
	#items2dArray = scipy.randn(numberOfItems, 2)
	#plotHierarchicalClustering(items2dArray, maxClusterCount, labelArray)
	items2dArray, labelArray = getInput()
	plotHierarchicalClustering(items2dArray, i, labelArray, 5)
'''

#hierarchicalClusterInput1.txt:
#yes, maxClusterCount:  27
#[551, 789, 814, 846, 881]

#hierarchicalClusterInput2.txt:
#yes, maxClusterCount:  28
#[193, 206, 233, 302, 825]

items2dArray, labelArray = getInput()
plotHierarchicalClustering(items2dArray, 27, labelArray, 5)
