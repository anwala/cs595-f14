#average similarity sorted by r
arrayOfItems = [551, 789, 814, 846, 881]
dictionaryOfPearsonSimilarity = {}

#pairwise pearson matrix
for item in arrayOfItems:
    dictionaryOfPearsonSimilarity[item] = [ sim_pearson(prefs, str(entry), str(item)) for entry in arrayOfItems if entry!=item]

raterAveragePearsonArrayOfTuples = []
for rater, pairwiseArray in dictionaryOfPearsonSimilarity.items():
    raterDataTuple = (rater, sum(pairwiseArray)/float(len(pairwiseArray)))
    raterAveragePearsonArrayOfTuples.append(raterDataTuple)
#sort
raterAveragePearsonArrayOfTuples = sorted(raterAveragePearsonArrayOfTuples, key=lambda tup: tup[1], reverse=True)
print raterAveragePearsonArrayOfTuples