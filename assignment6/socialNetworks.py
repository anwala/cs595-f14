#Install python-igraph: http://igraph.wikidot.com/installing-python-igraph-on-linux
#sudo add-apt-repository ppa:igraph/ppa
#sudo apt-get update
#sudo apt-get install python-igraph
import igraph

karateClubGraph = igraph.Graph.Read_GraphML('karate.GraphML')
folderName = 'graphs'
visual_style = {}
color_dict_vertices = {0: 'red', 1: 'green', 2: 'SkyBlue', 3: 'Gold', 4: 'DarkGray'}

def resetEdge():
	for edges in karateClubGraph.es:
		edges['edge_color'] = 'black'
		karateClubGraph.es["edge_width"] = 1

def girvinNewmanAlgorithm(maximumClusterThreshold):
	#calculate cluster
	clusters = karateClubGraph.clusters('weak')
	clusterCount = len(clusters)

	if( maximumClusterThreshold > 0 and maximumClusterThreshold >= clusterCount):
		iteration = 0
		while karateClubGraph.ecount() > 0 and clusterCount < maximumClusterThreshold and clusterCount < len(color_dict_vertices):

			clusters = karateClubGraph.clusters('weak')
			clusterCount = len(clusters)

			c = 0
			for cluster in clusters:
				for vertex in cluster:
					karateClubGraph.vs[vertex]['vertex_color'] = c
				c = c + 1

			#visual_style["vertex_color"] = [color_dict[node['Faction']] for node in karateClubGraph.vs]
			visual_style["vertex_color"] = [color_dict_vertices[node['vertex_color']] for node in karateClubGraph.vs]

			# calculate the edge betweenesses
			edgeBetweenness = karateClubGraph.edge_betweenness()

			# find the index of the edge with the maximum betweenness:http://lists.nongnu.org/archive/html/igraph-help/2008-11/msg00047.html
			indexOfEdgeWithMaximumBetweenness = max(xrange(len(edgeBetweenness)), key = edgeBetweenness.__getitem__)

			#modify edge color of edge with maximum betweenness
			karateClubGraph.es[indexOfEdgeWithMaximumBetweenness]['edge_color'] = 'blue'
			karateClubGraph.es[indexOfEdgeWithMaximumBetweenness]['edge_width'] = 5
			drawGraph('sn-' + str(iteration)+ '-' +str(clusterCount))

			#remove edge of maximum betweenness
			karateClubGraph.delete_edges(indexOfEdgeWithMaximumBetweenness)
			iteration = iteration + 1

def drawFactionsOriginal(filename):
	if( len(filename) > 0 ):
		color_dict = {1.0: 'red', 2.0: 'green'}
		visual_style["vertex_color"] = [color_dict[node['Faction']] for node in karateClubGraph.vs]
		visual_style['edge_color'] = [edgeColor for edgeColor in karateClubGraph.es['edge_color']]
		visual_style['edge_width'] = [edgeWidth for edgeWidth in karateClubGraph.es['edge_width']]

		layout = karateClubGraph.layout('rt_circular')#rt, rt_circular
		visual_style['layout'] = layout
		#visual_style["bbox"] = (300, 300)
		visual_style['margin'] = 20
		igraph.plot(karateClubGraph,'./'+folderName+'/'+filename+'.pdf', **visual_style)

def drawGraph(filename):

	if( len(filename) > 0 ):
		visual_style['edge_color'] = [edgeColor for edgeColor in karateClubGraph.es['edge_color']]
		visual_style['edge_width'] = [edgeWidth for edgeWidth in karateClubGraph.es['edge_width']]

		layout = karateClubGraph.layout('rt_circular')#rt, rt_circular
		visual_style['layout'] = layout
		#visual_style["bbox"] = (300, 300)
		visual_style['margin'] = 20
		igraph.plot(karateClubGraph,'./'+folderName+'/'+filename+'.pdf', **visual_style)


visual_style['vertex_label'] = karateClubGraph.vs['name']
resetEdge()

#draw original graph here
drawGraph('originalGraph')

#draw factions
drawFactionsOriginal('factionsGraph')

#centrality test here
girvinNewmanAlgorithm(5)
