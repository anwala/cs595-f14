#one vs. rest similarity for everyone
calculateSimilarItems(prefs, simMeasure, n=10, reverseSimilarityFlag=True, transformMatrixFlag=True):
    '''
    Create a dictionary of items showing which other items they are
    most similar to.
    '''
    result = {}
    # Invert the preference matrix to be item-centric

    if( transformMatrixFlag ):
        #with transform: movie top similarity
        itemPrefs = transformPrefs(prefs)
    else:
        #without transform: user top similarity
        itemPrefs = prefs

    for item in itemPrefs:
        scores = topMatches(itemPrefs, item, n=n, similarity=simMeasure, reverseSimilarityFlag=reverseSimilarityFlag)
        
        result[item] = scores
    return result