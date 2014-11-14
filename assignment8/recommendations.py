#!/usr/bin/python
# -*- coding: utf-8 -*-
from math import sqrt
import os, sys
# A dictionary of movie critics and their ratings of a small set of movies
critics = {
    'Lisa Rose': {
        'Lady in the Water': 2.5,
        'Snakes on a Plane': 3.5,
        'Just My Luck': 3.0,
        'Superman Returns': 3.5,
        'You, Me and Dupree': 2.5,
        'The Night Listener': 3.0,
    },
    'Gene Seymour': {
        'Lady in the Water': 3.0,
        'Snakes on a Plane': 3.5,
        'Just My Luck': 1.5,
        'Superman Returns': 5.0,
        'The Night Listener': 3.0,
        'You, Me and Dupree': 3.5,
    },
    'Michael Phillips': {
        'Lady in the Water': 2.5,
        'Snakes on a Plane': 3.0,
        'Superman Returns': 3.5,
        'The Night Listener': 4.0,
    },
    'Claudia Puig': {
        'Snakes on a Plane': 3.5,
        'Just My Luck': 3.0,
        'The Night Listener': 4.5,
        'Superman Returns': 4.0,
        'You, Me and Dupree': 2.5,
    },
    'Mick LaSalle': {
        'Lady in the Water': 3.0,
        'Snakes on a Plane': 4.0,
        'Just My Luck': 2.0,
        'Superman Returns': 3.0,
        'The Night Listener': 3.0,
        'You, Me and Dupree': 2.0,
    },
    'Jack Matthews': {
        'Lady in the Water': 3.0,
        'Snakes on a Plane': 4.0,
        'The Night Listener': 3.0,
        'Superman Returns': 5.0,
        'You, Me and Dupree': 3.5,
    },
    'Toby': {'Snakes on a Plane': 4.5, 'You, Me and Dupree': 1.0,
             'Superman Returns': 4.0},
}


# Returns a distance-based (Euclidean distance) similarity score for person1 and person2
# Note that this similarity score does not account for consistent grande inflation
# If one person tends to give higher grades than the other, even though both people
# might have similar tastes, their distance will be higher. Still, depending on the
# application, this might be what is expected
def sim_distance(prefs,person1,person2):
    # Get the list of shared_items
    si = {}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item]=1

    # if they have no ratins in common, return 0
    if len(si)==0: return 0

    # Add up the squares of all the differences
    sum_of_squares=sum([pow(prefs[person1][item]-prefs[person2][item],2) for item in si])

    return 1/(1+sqrt(sum_of_squares))


def sim_pearson(prefs,p1,p2):
    # Get the list of mutually rated shared_items
    si={}
    for item in prefs[p1]:
        if item in prefs[p2]: si[item]=1

    # Find the number of elements
    n=len(si)

    # if they have no ratings in common, return 0
    if n==0: return 0

    # Add up all the preferences
    sum1=sum([prefs[p1][it] for it in si])
    sum2=sum([prefs[p2][it] for it in si])

    # Sum up the squares
    sum1Sq=sum([pow(prefs[p1][it],2) for it in si])
    sum2Sq=sum([pow(prefs[p2][it],2) for it in si])

    # Sum up the products
    pSum=sum([prefs[p1][it]*prefs[p2][it] for it in si])

    # Calculate Pearson score
    num=pSum-(sum1*sum2/n)
    den=sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))
    if den==0: return 0

    r=num/den

    return r


# For more similarity metrics, http://en.wikipedia.org/wiki/Metric_%28mathematics%29#Examples
# Returns the best matches for person from the prefs dictionary
# Number of results and similarity function are optional params.
def topMatches(prefs,person,n=5,similarity=sim_pearson, reverseSimilarityFlag=True):
    scores=[(similarity(prefs,person,other),other) for other in prefs if other!=person]

    # Sort the list so the highest scores appear at the top
    scores.sort()

    if( reverseSimilarityFlag ):
        scores.reverse()

    return scores[0:n]


# Gets recommendations for a person by using a weighted average
# of every other user's rankings
def getRecommendations(prefs,person,similarity=sim_pearson):
    totals={}
    simSums={}
    for other in prefs:
        # don't compare me to myself
        if other==person: continue
        sim=similarity(prefs,person,other)

        # ignore scores of 0 or lower
        if sim<=0: continue
        for item in prefs[other]:

            # only score movies I haven't seen yet
            if item not in prefs[person] or prefs[person][item]==0:
                # Similarity * Score
                totals.setdefault(item,0)
                totals[item]+=prefs[other][item]*sim
                # Sum of similarities
                simSums.setdefault(item,0)
                simSums[item]+=sim

            # Create the normalized list
            rankings=[(total/simSums[item],item) for item,total in totals.items()]

            # Return the sorted list
            rankings.sort()
            rankings.reverse()
    return rankings



def transformPrefs(prefs):
    '''
    Transform the recommendations into a mapping where persons are described
    with interest scores for a given title e.g. {title: person} instead of
    {person: title}.
    '''

    result = {}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item, {})
            # Flip item and person
            result[item][person] = prefs[person][item]
    return result


def calculateSimilarItems(prefs, simMeasure, n=10, reverseSimilarityFlag=True, transformMatrixFlag=True):
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

    #c = 0
    for item in itemPrefs:

        # Status updates for large datasets
        #c += 1
        #if c % 100 == 0:
            #print '%d / %d' % (c, len(itemPrefs))
        # Find the most similar items to this one
        scores = topMatches(itemPrefs, item, n=n, similarity=simMeasure, reverseSimilarityFlag=reverseSimilarityFlag)
        
        result[item] = scores
    return result

#input:
    #prefs: [ userid, {'movie id': rating}, ...]
def calculateSimilarItems2(prefs, n=10, reverseSimilarityFlag=True):
    '''
    Create a dictionary of items showing which other items they are
    most similar to.
    '''

    result = {}
    # Invert the preference matrix to be item-centric

    itemPrefs = transformPrefs(prefs)
    #itemPrefs = prefs

    #user 344 rated 190 movies
    #without transform: user top similarity
    print len(prefs['344'])

    #movie 344 was rated by 55 users
    #with transform: movie top similarity
    print len(itemPrefs['344'])

    return
    #c = 0
    for item, value in itemPrefs.items():

        print 'key:', item, 'value:', value

        # Status updates for large datasets
        #c += 1
        #if c % 100 == 0:
            #print '%d / %d' % (c, len(itemPrefs))

        # Find the most similar items to this one
        scores = topMatches(itemPrefs, item, n=n, similarity=sim_distance, reverseSimilarityFlag=reverseSimilarityFlag)
        result[item] = scores

        print 'scores: ', scores

        break
    return result


def getRecommendedItems(prefs, itemMatch, user):
    userRatings = prefs[user]
    scores = {}
    totalSim = {}
    # Loop over items rated by this user
    for (item, rating) in userRatings.items():
        # Loop over items similar to this one
        for (similarity, item2) in itemMatch[item]:
            # Ignore if this user has already rated this item
            if item2 in userRatings:
                continue
            # Weighted sum of rating times similarity
            scores.setdefault(item2, 0)
            scores[item2] += similarity * rating
            # Sum of all the similarities
            totalSim.setdefault(item2, 0)
            totalSim[item2] += similarity
    # Divide each total score by total weighting to get an average
    rankings = [(score / totalSim[item], item) for (item, score) in
                scores.items()]
    # Return the rankings from highest to lowest
    rankings.sort()
    rankings.reverse()
    return rankings


def loadMovieLens(path='./data/movielens/'):
  # Get movie titles
    movies = {}
    for line in open(path + 'u.item'):
        (id, title) = line.split('|')[0:2]
        movies[id] = title
  # Load data
    prefs = {}
    for line in open(path + 'u.data'):
        (user, movieid, rating, ts) = line.split('\t')
        prefs.setdefault(user, {})
        #prefs[user][movies[movieid]] = float(rating)
        prefs[user][movieid] = float(rating)
    return prefs, movies

#output:
    #movies: <movie id, (movie title, ratingsArray)>
    #aggregateMovieData: [ (movie id, movie title, average movie rating, number of ratings) ]
    #aggregateUserData: [ (user id, gender, age, {'movie id': movie rating}) ]
def aggregateMovieAndUserData(path='./data/movielens/'):

    try:

        movies = {}
        aggregateMovieData = []
        for line in open(path + 'u.item'):
            (id, title) = line.split('|')[0:2]
            movies[id] = (title, [], -1)

        users = {}
        #populate user and movie data

        for line in open(path + 'u.data'):
            (user, movieid, rating, ts) = line.split('\t')

            user = user.strip()
            movieid = movieid.strip()
            rating = rating.strip()
            ts = ts.strip()

            users.setdefault(user, {})
            #movie title: movies[movieid][0]
            users[user][movieid] = float(rating)#key is movie title

            '''
            if( user in users ):
                users[user][movies[movieid][0]] = float(rating)
            else:
                users[user] = {}
            '''

            
            #movies[movieid]: (title, [ArrayOfRatings])
            #movies[movieid][0]: title
            #movies[movieid][1]: array of ratings
            movies[movieid][1].append(float(rating))



        #process movie data
        for movieId, tupleData in movies.items():
            averageRating = sum(tupleData[1]) / float(len(tupleData[1]))

            movietuples = (movieId, tupleData[0], averageRating, len(tupleData[1]))
            aggregateMovieData.append(movietuples)


        aggregateUserData = []
        for line in open(path + 'u.user'):
            (userId, age, gender, occupation, zipCode) = line.split('|')

            #userTuples: <userId, gender, age, {'movie title': movie rating}>
            userTuples = (userId, gender, age, users[userId])
            aggregateUserData.append(userTuples)
            

    except:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(fname, exc_tb.tb_lineno, sys.exc_info() )
        return



    return aggregateMovieData, aggregateUserData, movies


def getHighestRatedMovies(movies, count):

    if( count > 0 and count < len(movies) ):
        movies = sorted(movies, key=lambda tup: tup[2], reverse=True)
        i = 1
        for movie in movies:
            print movie

            if( i == count ):
                break
            i = i + 1

def getMostRatedMovies(movies, count):

    if( count > 0 and count < len(movies) ):
        movies = sorted(movies, key=lambda tup: tup[3], reverse=True)
        i = 1
        for movie in movies:
            print movie

            if( i == count ):
                break
            i = i + 1

#input:
    #aggregateUserData: [ (user id, gender, Age, {'movie id': movie rating}) ]
#output:
    #aggregateUsersFemale: [ (user id, F, Age, {'movie id': movie rating}) ]
    #aggregateUsersMale: [ (user id, M, Age, {'movie id': movie rating}) ]
def getFemaleAndMaleData(aggregateUsers):
    aggregateUsersFemale = []
    aggregateUsersMale = []
    if( len(aggregateUsers) > 0 ):

        for user in aggregateUsers:
            if( user[1] == 'F' ):
                aggregateUsersFemale.append(user)
            else:
                aggregateUsersMale.append(user)


    return aggregateUsersFemale, aggregateUsersMale


#output:
    #aggregateUsersFemale: [ (user id, F, {'movie id': movie rating}) ]
def getHighestRatedMoviesByMenOrWomen(aggregateUsersFemaleOrMale, count, movies):

    if( count > 0 and count < len(aggregateUsersFemaleOrMale) and len(movies) > 0):
        tupleOfMovieRatingDictionary = {}
        movieAverageRatingArrayOfTuples = []

        #aggregate ratings per movie
        for user in aggregateUsersFemaleOrMale:
            #userId: user[0]
            #gender: user[1]
            #Age: user[2]
            #<id,rating>: user[2]
            #tupleOfMovieRatingDictionary[]
            for movieid, rating in user[3].items():
                
                
                if( movieid in tupleOfMovieRatingDictionary ):
                    tupleOfMovieRatingDictionary[movieid].append(rating)
                else:
                    tupleOfMovieRatingDictionary[movieid] = []
                    tupleOfMovieRatingDictionary[movieid].append(rating)
                

        #average ratings
        for movie, ratingsArray in tupleOfMovieRatingDictionary.items():
            averageRating = sum(ratingsArray) / float(len(ratingsArray))

            movieRatingTuple = (movie, averageRating)
            movieAverageRatingArrayOfTuples.append(movieRatingTuple)

        #sort
        movieAverageRatingArrayOfTuples = sorted(movieAverageRatingArrayOfTuples, key=lambda tup: tup[1], reverse=True)

        i = 1
        for movieData in movieAverageRatingArrayOfTuples:
            print movies[ movieData[0] ][0], movieData[1]

            if( i == count ):
                break
            i = i + 1


#output:
    #aggregateUsersFemale: [ (user id, F, {'movie_title': movie rating}) ]
def getHighestRatedMoviesByMenOrWomenOverAge(aggregateUsersFemaleOrMale, count, ageLimit, movies):

    if( count > 0 and count < len(aggregateUsersFemaleOrMale) and ageLimit > 0 and len(movies) > 0 ):
        tupleOfMovieRatingDictionary = {}
        movieAverageRatingArrayOfTuples = []

        #aggregate ratings per movie
        for user in aggregateUsersFemaleOrMale:

            #if this person is beyond ageLimit
            if( int(user[2]) > ageLimit ):
                #userId: user[0]
                #gender: user[1]
                #Age: user[2]
                #<movie title,rating>: user[2]
                #tupleOfMovieRatingDictionary[]
                for movie, rating in user[3].items():
                    
                    if( movie in tupleOfMovieRatingDictionary ):
                        tupleOfMovieRatingDictionary[movie].append(rating)
                    else:
                        tupleOfMovieRatingDictionary[movie] = []
                        tupleOfMovieRatingDictionary[movie].append(rating)


        #average ratings
        for movie, ratingsArray in tupleOfMovieRatingDictionary.items():
            averageRating = sum(ratingsArray) / float(len(ratingsArray))

            movieRatingTuple = (movie, averageRating)
            movieAverageRatingArrayOfTuples.append(movieRatingTuple)

        #sort
        movieAverageRatingArrayOfTuples = sorted(movieAverageRatingArrayOfTuples, key=lambda tup: tup[1], reverse=True)

        i = 1
        for movieData in movieAverageRatingArrayOfTuples:
            print movies[movieData[0]][0], movieData[1]

            if( i == count ):
                break
            i = i + 1


#output:
    #aggregateUsersFemale: [ (user id, F, {'movie_title': movie rating}) ]
def getHighestRatedMoviesByMenOrWomenUnderAge(aggregateUsersFemaleOrMale, count, ageLimit, movies):

    if( count > 0 and count < len(aggregateUsersFemaleOrMale) and ageLimit > 0 and len(movies) > 0 ):
        tupleOfMovieRatingDictionary = {}
        movieAverageRatingArrayOfTuples = []

        #aggregate ratings per movie
        for user in aggregateUsersFemaleOrMale:

            #if this person is beyond ageLimit
            if( int(user[2]) < ageLimit ):
                #userId: user[0]
                #gender: user[1]
                #Age: user[2]
                #<movie title,rating>: user[2]
                #tupleOfMovieRatingDictionary[]
                for movie, rating in user[3].items():
                    
                    if( movie in tupleOfMovieRatingDictionary ):
                        tupleOfMovieRatingDictionary[movie].append(rating)
                    else:
                        tupleOfMovieRatingDictionary[movie] = []
                        tupleOfMovieRatingDictionary[movie].append(rating)


        
        #average ratings
        for movie, ratingsArray in tupleOfMovieRatingDictionary.items():
            averageRating = sum(ratingsArray) / float(len(ratingsArray))

            movieRatingTuple = (movie, averageRating)
            movieAverageRatingArrayOfTuples.append(movieRatingTuple)

        #sort
        movieAverageRatingArrayOfTuples = sorted(movieAverageRatingArrayOfTuples, key=lambda tup: tup[1], reverse=True)

        i = 1
        for movieData in movieAverageRatingArrayOfTuples:
            print movies[movieData[0]][0], movieData[1]

            if( i == count ):
                break
            i = i + 1

#input:
    #aggregateUsers: [ (user id, gender, Age, {'movie_title': movie rating}) ]
def getHighestMovieRaters(aggregateUsers, count):

    if( len(aggregateUsers) > 0 and count > 0 ):
        raterIDRatedMoviesCount = []

        for rater in aggregateUsers:

            #raterTuple: rater id, number of movies rated
            raterTuple = (rater[0], len(rater[3]))
            raterIDRatedMoviesCount.append(raterTuple)


        #sort
        raterIDRatedMoviesCount = sorted(raterIDRatedMoviesCount, key=lambda tup: tup[1], reverse=True)

        i = 1
        for rater in raterIDRatedMoviesCount:
            print rater[0], rater[1]

            if( i == count ):
                break
            i = i + 1

#http://stackoverflow.com/questions/5598181/python-print-on-same-line
def print_no_newline(string):
    import sys
    sys.stdout.write(string)
    sys.stdout.flush()

'''
def createNByNMatrix(arrayOfItems):
    if( len(arrayOfItems)> 0 ):

        dictOfItems = {}

        for item in arrayOfItems:
            dictOfItems[item]=[ result for entry in arrayOfItems if entry!=item]
'''         

aggregateMovies, aggregateUsers, movies = aggregateMovieAndUserData()


#1: What 5 movies have the highest average ratings? Show the movies and their ratings sorted by their average ratings.
#2: What 5 movies received the most ratings? Show the movies and the number of ratings sorted by number of ratings.

#getHighestRatedMovies(aggregateMovies, 10)
print ''
#getMostRatedMovies(aggregateMovies,10)




aggregateUsersFemale, aggregateUsersMale = getFemaleAndMaleData(aggregateUsers)
#3: What 5 movies were rated the highest on average by women? Show the movies and their ratings sorted by ratings.
#4: What 5 movies were rated the highest on average by men? Show the movies and their ratings sorted by ratings.


#getHighestRatedMoviesByMenOrWomen(aggregateUsersFemale, 5, movies)
print ''
#getHighestRatedMoviesByMenOrWomen(aggregateUsersMale, 5, movies)


#9: What movie was rated highest on average by men over 40? By men under 40?

'''
getHighestRatedMoviesByMenOrWomenOverAge(aggregateUsersMale, 5, 40, movies)
print ''
getHighestRatedMoviesByMenOrWomenUnderAge(aggregateUsersMale, 5, 40, movies)
'''


#10: What movie was rated highest on average by women over 40? By women under 40?
getHighestRatedMoviesByMenOrWomenOverAge(aggregateUsersFemale, 5, 40, movies)
print ''
getHighestRatedMoviesByMenOrWomenUnderAge(aggregateUsersFemale, 5, 40, movies)


#6: Which 5 raters rated the most films? Show the raters' IDs and the number of films each rated.
#getHighestMovieRaters(aggregateUsers, 5)


prefs, movies = loadMovieLens()
#5

'''
result1 = calculateSimilarItems(prefs=prefs, simMeasure=sim_pearson, n=10, reverseSimilarityFlag=True, transformMatrixFlag=True)

print movies['161'], 'most correlated:'
for r in result1['161']:
    rating = r[0]
    movieid = r[1]

    print '...', movies[movieid], rating

print ''

result2 = calculateSimilarItems(prefs=prefs, simMeasure=sim_pearson, n=10, reverseSimilarityFlag=False, transformMatrixFlag=True)
print movies['161'], ' least correlated:'
for r in result2['161']:
    rating = r[0]
    movieid = r[1]

    print '...', movies[movieid], rating
'''

#7
'''
#generates output to hierarchicalClusterInput1.txt for clustering
userSimilarityMatrix = calculateSimilarItems(prefs=prefs, simMeasure=sim_distance, n=5, reverseSimilarityFlag=False, transformMatrixFlag=False)

#for hierarchicalClustering.py input: reverseSimilarityFlag=False, sorts from smallest to largest
userSimilarityArrayOfTuples = []
for userId, userAttr in userSimilarityMatrix.items():

    print_no_newline(userId + ', ')

    for dist in userAttr:
        print_no_newline(str(dist[0]) + ', ')

    print ''

#yes, maxClusterCount:  27
#[551, 789, 814, 846, 881]
'''
#Part b

'''
#print prefs['551']
arrayOfItems = [551, 789, 814, 846, 881]
dictionaryOfPearsonSimilarity = {}

#pairwise pearson matrix
for item in arrayOfItems:
    dictionaryOfPearsonSimilarity[item] = [ sim_pearson(prefs, str(entry), str(item)) for entry in arrayOfItems if entry!=item]

raterAveragePearsonArrayOfTuples = []
for rater, pairwiseArray in dictionaryOfPearsonSimilarity.items():
    raterDataTuple = (rater, sum(pairwiseArray)/float(len(pairwiseArray)))
    raterAveragePearsonArrayOfTuples.append(raterDataTuple)

raterAveragePearsonArrayOfTuples = sorted(raterAveragePearsonArrayOfTuples, key=lambda tup: tup[1], reverse=True)
print raterAveragePearsonArrayOfTuples
'''
#8


'''
#generates output to hierarchicalClusterInput2.txt for clustering
userSimilarityMatrix = calculateSimilarItems(prefs=prefs, simMeasure=sim_distance, n=5, reverseSimilarityFlag=True, transformMatrixFlag=False)

#for hierarchicalClustering.py input: reverseSimilarityFlag=False, sorts from smallest to largest
userSimilarityArrayOfTuples = []
for userId, userAttr in userSimilarityMatrix.items():

    print_no_newline(userId + ', ')

    for dist in userAttr:
        print_no_newline(str(dist[0]) + ', ')

    print ''
'''

#part b



'''
arrayOfItems = [193, 206, 233, 302, 825]
dictionaryOfPearsonSimilarity = {}

#pairwise pearson matrix
for item in arrayOfItems:
    dictionaryOfPearsonSimilarity[item] = [ sim_pearson(prefs, str(entry), str(item)) for entry in arrayOfItems if entry!=item]

raterAveragePearsonArrayOfTuples = []
for rater, pairwiseArray in dictionaryOfPearsonSimilarity.items():
    raterDataTuple = (rater, sum(pairwiseArray)/float(len(pairwiseArray)))
    raterAveragePearsonArrayOfTuples.append(raterDataTuple)

raterAveragePearsonArrayOfTuples = sorted(raterAveragePearsonArrayOfTuples, key=lambda tup: tup[1], reverse=True)
print raterAveragePearsonArrayOfTuples
'''