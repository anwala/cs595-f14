import os, sys
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
import matplotlib.pyplot as plt
'''
	input: inputFileName.txt: <...,predicted label, actual label>
'''
def getListOfPredictedAndActualLabels(inputFileName):

	listOfPredictedLabels = []
	listOfActualLabels = []

	if( len(inputFileName) > 0 ):
		#print <classLabel, classLabelCount>
		try:
			inputFile = open(inputFileName, 'r')
			lines = inputFile.readlines()
			#first line is schema
			del lines[0]
			print len(lines), 'lines read from ' + inputFileName
			inputFile.close()
		except:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(fname, exc_tb.tb_lineno, sys.exc_info() )

	for l in lines:

		predictedAndActualLabel = l.split(', ')
		if( len(predictedAndActualLabel) > 1 ):

			predictedAndActualLabel = predictedAndActualLabel[-2:]

			predictedLabel = predictedAndActualLabel[0].strip()
			actualLabel = predictedAndActualLabel[1].strip()

			listOfPredictedLabels.append(predictedLabel)
			listOfActualLabels.append(actualLabel)

	return listOfPredictedLabels, listOfActualLabels



predictionFileName = '50nBlogTestDataSourcePredictions.txt'
listOfPredictedLabels, listOfActualLabels = getListOfPredictedAndActualLabels(predictionFileName)

'''
labels = ['a', 'b', 'c']
y_true = ['c', 'a', 'c', 'c', 'a', 'b']
y_pred = ['a', 'a', 'c', 'c', 'a', 'c']

confusionMatrix = confusion_matrix(y_true, y_pred, labels=labels)
precisionScore = precision_score(y_true, y_pred, average=None)
recallScore = recall_score(y_true, y_pred, average=None)
f1Score = f1_score(y_true, y_pred, average=None)
'''

labels = ['politics', 'story', 'law', 'misc']
confusionMatrix = confusion_matrix(listOfActualLabels, listOfPredictedLabels, labels=labels)
precisionScore = precision_score(listOfActualLabels, listOfPredictedLabels, labels=labels, average=None)
recallScore = recall_score(listOfActualLabels, listOfPredictedLabels, labels=labels, average=None)
f1Score = f1_score(listOfActualLabels, listOfPredictedLabels, labels=labels, average=None)

print confusionMatrix
print precisionScore

print recallScore
print f1Score


fig = plt.figure()
ax = fig.add_subplot(111)
cax = ax.matshow(confusionMatrix)
plt.title('Confusion Matrix of the Fischer Classifier')
fig.colorbar(cax)
ax.set_xticklabels([''] + labels)
ax.set_yticklabels([''] + labels)
plt.xlabel('Predicted')
plt.ylabel('True')
plt.show()