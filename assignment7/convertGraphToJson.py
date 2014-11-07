from bs4 import BeautifulSoup
import os, sys


try:
	inputFile = open('karate.GraphML', 'r')
	outputFile = open('karateClubGraph.json', 'w')

	htmlText = inputFile.read()
	inputFile.close()
except:
	exc_type, exc_obj, exc_tb = sys.exc_info()
	fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
	print fname, exc_tb.tb_lineno, sys.exc_info()


soup = BeautifulSoup(htmlText)
parentNodes = soup.findAll('node')

outputFile.write('{' + '\n')
outputFile.write('\t"nodes":' + '\n')
outputFile.write('\t[' + '\n')

if( len(parentNodes) > 0 ):

	for i in range(0, len(parentNodes)):
		factionAndNodeName = parentNodes[i].findAll('data')
		faction = factionAndNodeName[0].text
		nodeName = factionAndNodeName[1].text

		stringToWrite = '\t {"name": "' + nodeName + '", "faction": ' + faction + ', "color": 1 },' + '\n'
		#remove comma
		if( i == len(parentNodes)-1 ):
			stringToWrite = '\t {"name": "' + nodeName + '", "faction": ' + faction + ', "color": 1 }' + '\n'

		outputFile.write(stringToWrite)


	outputFile.write('\t],' + '\n')
	outputFile.write('\t"links":' + '\n')
	outputFile.write('\t[' + '\n')

parentEdges = soup.findAll('edge')
if( len(parentEdges) > 0 ):
	for i in range(0, len(parentEdges)):
		
		edgeWeight = parentEdges[i].find('data')
		#print edgeWeight.text

		#data = parentEdges[i].find('edge')
		sourceTargetDate = str(parentEdges[i])

		indexOfStart = sourceTargetDate.find('source="')
		indexOfEnd = sourceTargetDate.find('>')
		sourceTargetDate = sourceTargetDate[indexOfStart:indexOfEnd]

		sourceTargetDate = sourceTargetDate.split('"')
		sourceData = sourceTargetDate[1][1:]
		targetData = sourceTargetDate[3][1:]

		stringToWrite = '\t {"source": ' + sourceData + ', "target": ' + targetData + ', "weight": ' + edgeWeight.text + ', "id": "e' + str(i+1) + '" },\n'

		if( i == len(parentEdges)-1 ):
			stringToWrite = '\t {"source": ' + sourceData + ', "target": ' + targetData + ', "weight": ' + edgeWeight.text + ', "id": "e' + str(i+1) + '" }\n'

		outputFile.write(stringToWrite)

	outputFile.write('\t]' + '\n')
	outputFile.write('}' + '\n')

outputFile.close()