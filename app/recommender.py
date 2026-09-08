def genre_counter(liked_movies, watched_movies):
    genre_counts = {}

    #Count liked genres
    for movie in liked_movies:
        genres = movie.split(", ")
        for genre in genres:
            if genre in genre_counts:
                genre_counts[genre] += 2
            else:
                genre_counts.update({genre: 2})

    #Count watched genres
    for movie in watched_movies:
        genres = movie.split(", ")
        for genre in genres:
            if genre in genre_counts:
                genre_counts[genre] += 1
            else:
                genre_counts.update({genre: 1})
    
    return genre_counts

def director_counter(user):
    director_counts = {}

    for like in user.likes:
        director = like.movie.director
        if director in director_counts:
            director_counts[director] += 1
        else:
            director_counts.update({director: 1})
    
    return director_counts

def get_liked_actors(user):
    liked_actors = []

    for like in user.likes:
        actors = like.movie.actors
        liked_actors.append(actors)

    return liked_actors

def actor_counter(liked_actors):
    actor_counts = {}

    for actor_string in liked_actors:
        actors = actor_string.split(", ")
        for actor in actors:
            if actor in actor_counts:
                actor_counts[actor] += 1
            else:
                actor_counts.update({actor: 1})

    print("actor_counts:", actor_counts)
    return actor_counts

def get_user_genres(user):
    liked_movies = []
    watched_movies = []

    for like in user.likes:
        genres = like.movie.genres
        liked_movies.append(genres)

    for watch in user.watches:
        genres = watch.movie.genres
        watched_movies.append(genres)

    return genre_counter(liked_movies, watched_movies)


def score_movies(movie, genre_counts, director_counts, actor_counts):
    score = 0

    genres = movie.genres.split(", ")
    director = movie.director
    actors = movie.actors.split(", ")

    for genre in genres:
        if genre in genre_counts:
            score += genre_counts[genre]

    if director in director_counts:
        score += director_counts[director] * 2

    for actor in actors:
        if actor in actor_counts:
            score += actor_counts[actor] * 1.5

    return score

def get_recommendations(movies, genre_counts, director_counts, actor_counts, user):

    #Get watches / likes
    watched_or_liked = set()

    for like in user.likes:
        watched_or_liked.add(like.movie_id)

    for watch in user.watches:
        watched_or_liked.add(watch.movie_id)

    recommendations = []

    for movie in movies:
        if movie.id in watched_or_liked:
            continue
        score = score_movies(movie, genre_counts, director_counts, actor_counts)

        if score == 0:
            continue

        recommendations.append({"movie": movie, "score": score})

    recommendations.sort(key=lambda x: x["score"], reverse=True)

    return recommendations[:5]