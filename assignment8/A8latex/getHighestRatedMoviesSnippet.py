#get highest rated movies
def getHighestRatedMovies(movies, count):
    if( count > 0 and count < len(movies) ):
        movies = sorted(movies, key=lambda tup: tup[2], reverse=True)
        i = 1
        for movie in movies:
            print movie

            if( i == count ):
                break
            i = i + 1