#aggregate data
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