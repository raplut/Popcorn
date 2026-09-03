def genre_counter(liked_movies):
    genre_counts = {}

    for movie in liked_movies:
        genres = movie.split(", ")
        for genre in genres:
            if genre in genre_counts:
                genre_counts[genre] += 1
            else:
                genre_counts.update({genre: 1})
    
    return genre_counts

def get_liked_genres(user):
    liked_movies = []

    for like in user.likes:
        genres = like.movie.genres
        liked_movies.append(genres)

    return genre_counter(liked_movies)


def score_movies(movie, genre_counts):
    score = 0

    genres = movie.genres.split(", ")

    for genre in genres:
        if genre in genre_counts:
            score += genre_counts[genre]

    return score

def get_recommendations(movie, genre_counts, user):

    #Get watches / likes
    watched_or_liked = set()

    for like in user.likes:
        watched_or_liked.add(like.movie_id)

    for watch in user.watches:
        watched_or_liked.add(watch.movie_id)

    print("watched_or_liked:", watched_or_liked)

    recommendations = []

    for movie in movie:
        if movie.id in watched_or_liked:
            continue
        score = score_movies(movie, genre_counts)

        recommendations.append({"movie": movie, "score": score})

    recommendations.sort(key=lambda x: x["score"], reverse="True")

    return recommendations