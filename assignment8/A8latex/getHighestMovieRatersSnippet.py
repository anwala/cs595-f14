#get highest movie raters
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