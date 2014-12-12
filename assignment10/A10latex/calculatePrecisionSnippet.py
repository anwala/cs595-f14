#calculate precision, recall, f1 score, and plot confusion matrix
predictionFileName = '50nBlogTestDataSourcePredictions.txt'
listOfPredictedLabels, listOfActualLabels = getListOfPredictedAndActualLabels(predictionFileName)

labels = ['politics', 'story', 'law', 'misc']
confusionMatrix = confusion_matrix(listOfActualLabels, listOfPredictedLabels, labels=labels)
precisionScore = precision_score(listOfActualLabels, listOfPredictedLabels, average=None)
recallScore = recall_score(listOfActualLabels, listOfPredictedLabels, average=None)
f1Score = f1_score(listOfActualLabels, listOfPredictedLabels, average=None)

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