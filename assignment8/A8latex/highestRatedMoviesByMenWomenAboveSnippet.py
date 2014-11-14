#higest rated movies by women/men above age
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