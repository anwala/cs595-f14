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