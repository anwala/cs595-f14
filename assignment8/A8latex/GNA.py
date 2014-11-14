#Girvin-Newman Algorithm For Community Detection
def girvinNewmanAlgorithm(maximumClusterThreshold):
...
	while karateClubGraph.ecount() > 0 and clusterCount < maximumClusterThreshold...):

		clusters = karateClubGraph.clusters('weak')
		clusterCount = len(clusters)

		visual_style["vertex_color"] = [color_dict_vertices[node['vertex_color']] for node in karateClubGraph.vs]

		# calculate the edge betweenesses
		edgeBetweenness = karateClubGraph.edge_betweenness()

		# find the index of the edge with the maximum betweenness:http://lists.nongnu.org/archive/html/igraph-help/2008-11/msg00047.html
		indexOfEdgeWithMaximumBetweenness = max(xrange(len(edgeBetweenness)), key = edgeBetweenness.__getitem__)

		#modify edge color of edge with maximum betweenness
		karateClubGraph.es[indexOfEdgeWithMaximumBetweenness]['edge_color'] = 'blue'
		karateClubGraph.es[indexOfEdgeWithMaximumBetweenness]['edge_width'] = 5
		drawGraph('social_network' + str(iteration)+ '_' +str(clusterCount))

		#remove edge of maximum betweenness
		karateClubGraph.delete_edges(indexOfEdgeWithMaximumBetweenness)
		iteration = iteration + 1
...